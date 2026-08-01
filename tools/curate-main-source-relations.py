#!/usr/bin/env python3
"""Curate the bounded main-source relation for each Return of Zero section."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml


RELATIONS: dict[str, list[str]] = {
    "bratton-2026-agentworld-brief": [
        "§0/1 · contemporary horizon and action–model problem",
        "§0 · objective-internality and active-context return",
        "§5 · research target and agentworld constraint",
        "§5→0 · submission problem-field return",
    ],
    "pind-2009-dignaga-anyapoha-dissertation": [
        "§0/1 · determination by conceptual exclusion",
        "§0 · apoha movement",
    ],
    "spinoza-1674-letter-50-jelles": ["§0/1 · finite determination and negation"],
    "raatikainen-2026-godel-incompleteness-sep": [
        "§0/1 · scoped formal-limit warrant"
    ],
    "gebser-1985-ever-present-origin": [
        "§0/1 · diaphaneity and integral demand",
        "§4 · Apollo–Dionysus and integral return",
    ],
    "frank-gleiser-thompson-2024-blind-spot": [
        "§0/1 · experiencer and lifeworld counterpressure"
    ],
    "bohm-1980-wholeness-implicate-order": [
        "§0 · implication–explication process bridge"
    ],
    "dyczkowski-2000-doctrine-vibration": [
        "§0 · Spanda and tattvic differentiation spine"
    ],
    "abhinavagupta-singh-1988-paratrisika-vivarana": [
        "§0 · primary differentiation and recognition carrier"
    ],
    "isvarakrishna-colebrooke-wilson-1837-sankhya-karika": [
        "§0 · inner-instrument functional distinctions"
    ],
    "kaplan-1999-nothing-that-is": ["§1 · narrative and learning spine"],
    "colebrooke-1817-brahmagupta-bhaskara": [
        "§1 · primary zero arithmetic and zero-denominator verses"
    ],
    "dutta-2023-zero-divided-numbers-india": [
        "§1 · specialist history and cancellation-regime corrective"
    ],
    "rotman-1987-signifying-nothing": [
        "§1 · absence-to-operative-inscription semiotic bridge"
    ],
    "taylor-2026-core-theorems-pithy": [
        "§2 · native two-logics derivation",
        "§3 · eight-determination and theorem spine",
    ],
    "jung-2013-undiscovered-self-routledge": [
        "§2 · mass, State, and statistical-abstraction pressure"
    ],
    "desmet-2022-psychology-totalitarianism-web-essay": [
        "§2 · mass-formation formulation"
    ],
    "iakovou-2022-misuse-totalitarianism": [
        "§2 · institutional counterpressure to psychologisation"
    ],
    "daza-et-al-2016-basin-entropy": [
        "§2 · nonlinear basin and bifurcation mechanism"
    ],
    "taylor-2026-ql-musical-derivation-v3": [
        "§3 · internal formal-musical derivation"
    ],
    "kauffman-2014-iterants-fermions-dirac-arxiv": [
        "§3 · iterant and re-entry temporalisation"
    ],
    "nist-dlmf-2026-complex-variable": [
        "§3 · complex and projective technical floor"
    ],
    "hatcher-2002-algebraic-topology": ["§3 · torus, cover, and winding reference"],
    "scholtz-1998-algorithms-diatonic-keyboard-tunings": [
        "§3 · tuning and commas mathematical witness"
    ],
    "jung-pauli-meier-2001-atom-archetype": [
        "§4 · primary psychoid and number historical carrier"
    ],
    "atmanspacher-2020-pauli-jung-conjecture": [
        "§4 · dual-aspect formulation and limit"
    ],
    "jung-1978-aion-cw9-2": ["§4 · X=x and quaternity primary work"],
    "lacan-2017-talking-to-brick-walls": ["§4 · primary wall and signifier scene"],
    "darmon-1992-matheme-ali": ["§4 · matheme definition and transmission"],
    "vaswani-et-al-2017-attention": ["§5 · transformer and attention baseline"],
    "pytorch-2-9-softmax-argmax-api": ["§5 · exact softmax and argmax mechanism"],
    "lecun-et-al-2006-energy-based-learning": [
        "§5 · J-space and Bimba energy-field technical spine"
    ],
    "bradley-terry-1952-paired-comparisons": [
        "§5 · paired-comparison preference baseline"
    ],
    "rafailov-et-al-2023-dpo": ["§5 · contemporary preference optimisation"],
    "freeth-et-al-2021-model-cosmos": [
        "§5→0 · Antikythera reconstruction and attunement anchor"
    ],
    "42-techne-2026-sovereign-commons": ["§5→0 · applied 4:2 Technē architecture"],
    "ostrom-2009-beyond-markets-states-nobel-lecture": [
        "§5→0 · polycentric governance warrant and qualification"
    ],
    "bohm-1996-on-dialogue": ["§5→0 · meaning-through-relation precedent"],
    "berkeley-1734-three-dialogues-wilkins-2002": [
        "§5→0 · bounded idealist-horizon primary source"
    ],
}

SECTIONS = {"§0/1", "§0", "§1", "§2", "§3", "§4", "§5", "§5→0"}
FRONTMATTER_RE = re.compile(r"^---\n(?P<yaml>.*?)\n---\n", re.DOTALL)


def load_house(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")
    data = yaml.safe_load(match.group("yaml")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    return data, text[match.end() :]


def render(data: dict, body: str) -> str:
    payload = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000).rstrip()
    return f"---\n{payload}\n---\n{body}"


def expected_outputs(root: Path) -> dict[Path, str]:
    source_root = root / "essay-workshop" / "sources-texts-references" / "source-bank" / "sources"
    houses = {path.parent.name: path for path in source_root.glob("*/SOURCE.md")}
    missing = sorted(set(RELATIONS) - set(houses))
    if missing:
        raise ValueError("main-source relation names missing houses: " + ", ".join(missing))
    covered = {relation.split(" · ", 1)[0] for rows in RELATIONS.values() for relation in rows}
    if covered != SECTIONS:
        raise ValueError(f"section coverage mismatch: expected {sorted(SECTIONS)}, got {sorted(covered)}")

    outputs: dict[Path, str] = {}
    for source_id in sorted(RELATIONS):
        path = houses[source_id]
        data, body = load_house(path)
        data["main_source_for"] = RELATIONS[source_id]
        outputs[path] = render(data, body)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    try:
        outputs = expected_outputs(root)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    stale = [path for path, content in outputs.items() if path.read_text(encoding="utf-8") != content]
    if args.check:
        for path in stale:
            print(f"stale:{path.relative_to(root)}", file=sys.stderr)
        if stale:
            return 1
        print(f"Main-source relations current: {len(RELATIONS)} sources across {len(SECTIONS)} sections.")
        return 0
    for path in stale:
        content = outputs[path]
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temp:
            temp.write(content)
            temp_path = Path(temp.name)
        temp_path.replace(path)
    print(f"Curated {len(RELATIONS)} main sources across {len(SECTIONS)} sections; changed {len(stale)} houses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
