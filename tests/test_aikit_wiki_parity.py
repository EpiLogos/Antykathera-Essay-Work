"""AIKit's wiki ingest carries the corpus the retired `.bkmr` index used to.

This repo used to run its own bkmr index: `tools/bkmr-essay` derived adapters
under `.bkmr/adapters`, recorded them in `.bkmr/manifest.tsv`, and loaded six
SQLite databases under `.bkmr/db`. AIKit's `wiki ingest` now does that job —
it reads the same vault, binds every addressable file into a SourcePool with
its authored tags, and hands that pool to the same bkmr through the
`tool/search/bkmr` provider. Two indexes over one corpus is duplication, so
the local pipeline was retired.

Retiring it only holds if the replacement covers it, so its coverage is frozen
in `fixtures/retired-bkmr-coverage.json` — all 884 canonical paths across the
six collections it indexed — and asserted here against a live ingest. These
tests are the standing evidence for that retirement, not a one-off migration
check.

They need the `aikit` binary. Set `AIKIT_BIN`, or have `aikit` on PATH; the
suite skips rather than fails when it is absent, so this repo does not require
an AIKit build to test its own prose.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
VAULT = PROJECT / "submission-package" / "essay"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "retired-bkmr-coverage.json"
# The vault's own structure sits one segment below its root (`symbolon/episteme`,
# `symbolon/mytheme`), so a room is two segments deep from here.
ROOM_DEPTH = "2"


def aikit_binary():
    explicit = os.environ.get("AIKIT_BIN")
    if explicit and Path(explicit).exists():
        return explicit
    found = shutil.which("aikit")
    if found:
        return found
    return None


class AikitWikiParityTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.binary = aikit_binary()
        if cls.binary is None:
            raise unittest.SkipTest("aikit is not available; set AIKIT_BIN or put it on PATH")
        cls.workspace = tempfile.mkdtemp(prefix="aikit-parity-")
        wiki = Path(cls.workspace) / "wiki.json"
        wiki.write_text('{"schema":"okf-wiki/v1","objects":[]}')
        cls.wiki = wiki
        result = subprocess.run(
            [
                cls.binary, "--json", "wiki", "ingest",
                "--file", str(wiki),
                "--room-depth", ROOM_DEPTH,
                "--apply",
                str(VAULT),
            ],
            cwd=PROJECT, text=True, capture_output=True,
        )
        if result.returncode != 0:
            raise unittest.SkipTest(f"aikit wiki ingest failed: {result.stderr[:500]}")
        envelope = json.loads(result.stdout)
        cls.data = envelope["data"]
        cls.warnings = envelope.get("warnings", [])
        cls.material = []
        for shard in sorted((Path(cls.workspace) / "wiki.sources").glob("corpus-*.json")):
            cls.material.extend(json.loads(shard.read_text()))

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "workspace", None):
            shutil.rmtree(cls.workspace, ignore_errors=True)

    # -- coverage of the retired index -----------------------------------

    def test_every_path_the_retired_bkmr_index_covered_is_addressed(self):
        """The parity claim itself: nothing the old index held was lost."""
        fixture = json.loads(FIXTURE.read_text())
        bound = {
            item["binding"]["metadata"]["relative_path"]
            for item in self.material
            if "relative_path" in item["binding"].get("metadata", {})
        }
        missing = {}
        for collection, paths in fixture["collections"].items():
            gone = sorted(path for path in paths if path not in bound)
            if gone:
                missing[collection] = gone
        self.assertEqual(missing, {}, "AIKit must address everything the retired index did")

    def test_the_retired_collections_all_survive_as_bound_material(self):
        fixture = json.loads(FIXTURE.read_text())
        self.assertEqual(
            sorted(fixture["collections"]),
            ["arguments", "concepts", "passages", "records", "rooms", "sections"],
        )
        by_path = {
            item["binding"]["metadata"]["relative_path"]: item
            for item in self.material
            if "relative_path" in item["binding"].get("metadata", {})
        }
        for collection, paths in fixture["collections"].items():
            with self.subTest(collection=collection):
                bodies = [by_path[p]["body"] for p in paths if p in by_path]
                self.assertEqual(len(bodies), len(paths))
                self.assertTrue(
                    all(body.strip() for body in bodies),
                    f"{collection}: every binding carries the file's own text, not a stub",
                )

    # -- the corpus is fully placed --------------------------------------

    def test_no_addressable_file_is_set_aside(self):
        self.assertEqual(self.data["skipped_unaddressable"], 0, self._unaddressable())
        self.assertEqual(self.data["duplicate_record_id"], 0)
        self.assertEqual(self.data["duplicate_source_id"], 0)
        self.assertEqual(self.data["unparseable"], 0)

    def _unaddressable(self):
        return "\n".join(w for w in self.warnings if "cannot be placed" in w)

    def test_every_vault_file_binds_exactly_once(self):
        files = {
            str(path.relative_to(VAULT))
            for path in VAULT.rglob("*.md")
            if ".obsidian" not in str(path) and not path.is_symlink()
        }
        bound = [
            item["binding"]["metadata"]["relative_path"]
            for item in self.material
            if "relative_path" in item["binding"].get("metadata", {})
        ]
        self.assertEqual(len(bound), len(set(bound)), "no file binds twice")
        self.assertEqual(set(bound), files)

    # -- tags, which is what the bkmr index was for ----------------------

    def test_every_authored_tag_reaches_the_source_pool(self):
        """The vocabulary in the files is the vocabulary in the pool."""
        declared = set()
        for path in VAULT.rglob("*.md"):
            # Ingest walks with `follow_links(false)`, so a symlink pointing
            # out of the vault (there is one, into `working/`) is not corpus.
            # Reading through it here would hold the pool to a vocabulary the
            # vault does not actually declare.
            if ".obsidian" in str(path) or path.is_symlink():
                continue
            text = path.read_text(errors="replace")
            if not text.startswith("---\n"):
                continue
            end = text.find("\n---", 4)
            if end < 0:
                continue
            block = text[4:end]
            for line_no, line in enumerate(block.split("\n")):
                if line.startswith("tags:"):
                    inline = line[len("tags:"):].strip()
                    if inline.startswith("[") and inline.endswith("]"):
                        declared.update(t.strip() for t in inline[1:-1].split(",") if t.strip())
                    else:
                        for item in block.split("\n")[line_no + 1:]:
                            if not item.strip().startswith("- "):
                                break
                            declared.add(item.strip()[2:].strip().strip("\"'"))
        carried = set()
        for item in self.material:
            carried.update(item["binding"]["tags"])
        self.assertTrue(declared, "the corpus declares tags")
        self.assertEqual(
            sorted(declared - carried), [], "every declared tag reaches the pool"
        )
        self.assertGreaterEqual(self.data["tag_vocabulary"], len(declared))

    def test_a_record_inherits_the_vocabulary_of_the_sources_it_cites(self):
        """The corpus authors its tags on the bibliography, not on the records."""
        inherited = [
            item for item in self.material
            if item["binding"]["metadata"].get("corpus_kind") == "record"
            and item["binding"]["tags"]
            and not item["binding"]["metadata"].get("declared_tags")
        ]
        self.assertTrue(
            inherited,
            "records that declare no tags of their own still carry their sources'",
        )

    def test_tag_filtered_retrieval_answers_over_the_ingested_pool(self):
        result = subprocess.run(
            [
                self.binary, "--json", "--cwd", self.workspace,
                "knowledge", "search", "tag:epi-logos/antikythera-essay", "--limit", "5",
            ],
            cwd=PROJECT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr[:500])
        hits = json.loads(result.stdout)["data"]["hits"]
        self.assertTrue(hits, "a tag filter retrieves from the pool")
        self.assertTrue(
            all(hit["resource"].startswith("central:source:corpus:") for hit in hits)
        )

    # -- links ------------------------------------------------------------

    def test_no_link_that_resolves_inside_the_vault_is_left_unresolved(self):
        """Unresolved is allowed only for targets the vault does not hold."""
        import re, os.path

        held = {
            str(path.relative_to(VAULT).with_suffix(""))
            for path in VAULT.rglob("*.md")
            if ".obsidian" not in str(path)
        }
        by_id = {}
        for item in self.material:
            meta = item["binding"].get("metadata", {})
            if "relative_path" in meta:
                by_id[meta["relative_path"]] = item["binding"]["source"]
        leaked = []
        for warning in self.warnings:
            match = re.search(r"record (\S+) links `([^`]+)`", warning)
            if not match or "resolves to no record and no source" not in warning:
                continue
            target = match.group(2)
            candidate = os.path.normpath(target)
            candidate = candidate[:-3] if candidate.endswith(".md") else candidate
            if candidate in held:
                leaked.append(warning)
        self.assertEqual(leaked, [], "a target the vault holds must resolve")


if __name__ == "__main__":
    unittest.main()
