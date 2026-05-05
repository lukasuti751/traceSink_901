from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ms-dos_new" / "main.py"
OUT.parent.mkdir(parents=True, exist_ok=True)

topics = [
    "bound external calls with try/catch when sink is untrusted",
    "prefer pull over push payments on mainnet cohort systems",
    "use voltNonReentrant on operator paths that touch drills",
    "keep publishLesson gas hints inside GAS_HINT_FLOOR..CEILING",
    "never key access control off tx.origin on EVM",
    "document cohort pacing to mitigate griefing bursts",
    "seal lessons once curriculum is immutable",
    "emit audit digests off-chain for SIEM correlation",
    "separate governor from operator from auditor roles",
    "test reviveDrill only after incident response sign-off",
    "saturatingAdd models wrap-safe accumulation drills",
    "boundedMul enforces cap discipline in pure probes",
    "facet probes are pure; keep state changes in guarded paths",
    "traceSink may revert; handle VDL_SinkReverted paths",
    "ADDRESS_A/B/C are immutables; rotate via new deployment if compromised",
    "avoid unbounded loops in receive/fallback paths",
    "reject ETH via empty receive to avoid accidental custody",
    "use OpenZeppelin Timelock if governance rotation needs delay",
    "pair this UI with formal reviews before mainnet",
    "rate-limit learnerPulse off-chain as well as on-chain pacing",
]

facets = []
bases = "ALPHA BRAVO CHARLIE DELTA ECHO FOXTROT GOLF HOTEL INDIA JULIETT KILO LIMA MIKE NOVEMBER OSCAR PAPA QUEBEC ROMEO SIERRA TANGO UNIFORM VICTOR WHISKEY XRAY YANKEE ZULU".split()
for b in bases:
    for j in range(22):
        facets.append(f"{b}{j}")

tips = []
for i in range(920):
    t = topics[i % len(topics)]
    tips.append(
        f"{i:04d}: {t}; facet echo {facets[i % len(facets)]} salt {hex((0xC0FFEE ^ i * 1315423911) & 0xFFFFFFFF)}"
    )

tips_literal = "TIPS: Tuple[str, ...] = (\n" + ",\n".join(repr(t) for t in tips) + "\n)\n"

core = '''# -*- coding: utf-8 -*-
"""ms-dos_new — VoltTrace / explos_dos pedagogy shell (AI hack learning tool)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shlex
import sys
import textwrap
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

TRACE_VERSION = 0x7A3C91F0E4B2D816
DRILL_SEED = 0x4F2E9C1A7B5583D4
DEFAULT_RPC = os.environ.get("VOLT_RPC_URL", "")

ADDRESS_A = "0x352F4Aee77Fd288EA8F977b7418bb0402e5EF709"
ADDRESS_B = "0x46acda232073817355080066FB593fc3DE858078"
ADDRESS_C = "0x6c7cA6dA7FD60AAbCF155B1d4D8AdbEb18c32773"

'''

core += tips_literal + "\n"

core += textwrap.dedent(
    '''
@dataclass
class LessonCard:
    lid: int
    title: str
    gas_hint: int
    notes: str = ""


@dataclass
class CohortCard:
    cid: int
    tag_hex: str
    cap: int
    members: List[str] = field(default_factory=list)


@dataclass
class VoltSession:
    cwd: Path = field(default_factory=lambda: Path.cwd())
    history: List[str] = field(default_factory=list)
    lessons: Dict[int, LessonCard] = field(default_factory=dict)
    cohorts: Dict[int, CohortCard] = field(default_factory=dict)
    env: Dict[str, str] = field(default_factory=dict)
    rng: random.Random = field(default_factory=lambda: random.Random(DRILL_SEED))

    def __post_init__(self) -> None:
        self.env.setdefault("PROMPT", "VOLT>")
        self.env.setdefault("TRACE", "1")
        self._seed_demo()
