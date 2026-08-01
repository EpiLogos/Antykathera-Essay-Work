import json
import tempfile
import unittest
from email.message import Message
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import download_section_images as downloader


class DownloaderTests(unittest.TestCase):
    def test_manifest_is_valid_and_section_slugs_match_folder_names(self):
        manifest = downloader.load_manifest(ROOT / "image-manifest.json")
        sections = list(downloader.iter_sections(manifest))

        self.assertGreaterEqual(len(sections), 10)
        self.assertEqual("edge-of-the-rational", sections[1].slug)
        self.assertEqual(sections[1].slug, downloader.slugify(sections[1].slug))

    def test_license_filter_rejects_non_free_usage_terms(self):
        record = {
            "imageinfo": {
                "extmetadata": {
                    "UsageTerms": {"value": "Non-free fair use only"},
                    "LicenseShortName": {"value": "Fair use"},
                }
            }
        }

        self.assertFalse(downloader.license_allowed(record, ["fair use", "non-free"]))

    def test_relevance_scoring_uses_title_description_symbols_and_image_mime(self):
        section = downloader.Section(
            slug="images-that-constellate",
            title="The Images That Constellate",
            visual_intent="",
            symbols=["Lorenz attractor", "crystal lattice"],
            queries=["Lorenz attractor"],
        )
        record = {
            "title": "File:Lorenz attractor.svg",
            "imageinfo": {
                "mime": "image/svg+xml",
                "width": 1200,
                "height": 800,
                "extmetadata": {
                    "ImageDescription": {
                        "value": "A diagram of the Lorenz strange attractor in phase space."
                    },
                    "Categories": {"value": "Chaos theory; Attractors"},
                },
            },
        }

        self.assertGreaterEqual(downloader.relevance_score(record, "Lorenz attractor", section), 10)

    def test_build_record_preserves_provenance_fields(self):
        section = downloader.Section("edge", "Edge", "", ["Goedel"], ["Kurt Goedel portrait"])
        record = {
            "title": "File:Kurt Goedel portrait.jpg",
            "imageinfo": {
                "url": "https://upload.wikimedia.org/example.jpg",
                "mime": "image/jpeg",
                "width": 1600,
                "height": 1000,
                "extmetadata": {
                    "ImageDescription": {"value": "<p>Portrait of Kurt Goedel</p>"},
                    "Artist": {"value": "Unknown"},
                    "LicenseShortName": {"value": "Public domain"},
                    "UsageTerms": {"value": "Public domain"},
                },
            },
        }

        output = downloader.build_record(record, section, "Kurt Goedel portrait", 9, "goedel.jpg")

        self.assertEqual(output["filename"], "goedel.jpg")
        self.assertIn("commons.wikimedia.org/wiki/File:Kurt_Goedel_portrait.jpg", output["source_url"])
        self.assertEqual(output["license"], "Public domain")
        self.assertEqual(output["description"], "Portrait of Kurt Goedel")

    def test_validate_manifest_rejects_duplicate_section_slugs(self):
        manifest = {
            "sections": [
                {
                    "slug": "same",
                    "title": "A",
                    "visual_intent": "x",
                    "symbols": [],
                    "queries": ["one"],
                },
                {
                    "slug": "same",
                    "title": "B",
                    "visual_intent": "x",
                    "symbols": [],
                    "queries": ["two"],
                },
            ]
        }

        with self.assertRaises(ValueError):
            downloader.validate_manifest(manifest)

    def test_write_report_contains_sources_and_mode(self):
        row = {
            "filename": "image.jpg",
            "score": 7,
            "title": "File:Image.jpg",
            "query": "test image",
            "license": "CC BY-SA 4.0",
            "usage_terms": "",
            "source_url": "https://commons.wikimedia.org/wiki/File:Image.jpg",
        }
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            downloader.write_report(report, [row], dry_run=True)
            text = report.read_text(encoding="utf-8")

        self.assertIn("Mode: dry run", text)
        self.assertIn("CC BY-SA 4.0", text)
        self.assertIn("https://commons.wikimedia.org/wiki/File:Image.jpg", text)

    def test_ssl_context_uses_a_verified_default_context(self):
        context = downloader.ssl_context()

        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode.name, "CERT_REQUIRED")

    def test_retry_after_seconds_respects_header(self):
        headers = Message()
        headers["Retry-After"] = "4"
        exc = downloader.urllib.error.HTTPError("https://example.test", 429, "Too Many Requests", headers, None)

        self.assertEqual(downloader.retry_after_seconds(exc, 0), 4.0)

    def test_parse_args_accepts_repeated_excluded_sections(self):
        args = downloader.parse_args(["--exclude-section", "a", "--exclude-section", "b"])

        self.assertEqual(args.exclude_section, ["a", "b"])

    def test_parse_args_defaults_to_continue_on_download_error(self):
        args = downloader.parse_args([])

        self.assertFalse(args.fail_fast)

    def test_read_existing_titles_ignores_bad_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            metadata = Path(tmp) / "metadata.jsonl"
            metadata.write_text('{"title": "File:A.jpg"}\nnot json\n{"title": "File:B.jpg"}\n', encoding="utf-8")

            titles = downloader.read_existing_titles(metadata)

        self.assertEqual(titles, {"File:A.jpg", "File:B.jpg"})


if __name__ == "__main__":
    unittest.main()
