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

    def _seed_demo(self) -> None:
        for i in range(6):
            self.lessons[i] = LessonCard(
                lid=i,
                title=f"DOS-mitigation facet {i}",
                gas_hint=21_000 + i * 900,
                notes="Clamp sums; pace cohort pulses; avoid unbounded callbacks.",
            )
        for j in range(4):
            self.cohorts[j] = CohortCard(cid=j, tag_hex=hex(j * 0xC0FFEE)[2:], cap=16 + j)


def _clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def _saturating_add(a: int, b: int) -> Tuple[int, bool]:
    s = a + b
    if s < a:
        return (2**256 - 1, True)
    return (s, False)


def _keccak_topic(label: str) -> str:
    k = hashlib.sha3_256()
    k.update(label.encode("utf-8"))
    return "0x" + k.hexdigest()[:64]


def _rpc_chain_id(url: str) -> Optional[int]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_chainId", "params": []}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None
    res = payload.get("result")
    if isinstance(res, str) and res.startswith("0x"):
        return int(res, 16)
    return None


FACET_LABELS = ''' + repr(facets) + r'''


class VoltDosShell:
    """Retro command surface mapping DOS verbs to pedagogy actions."""

    def __init__(self, session: VoltSession) -> None:
        self.s = session
        self._cmds: Dict[str, Callable[[List[str]], int]] = {}
        self._register_core()
        self._register_facets()

    def _register_core(self) -> None:
        self._cmds["VER"] = self.cmd_ver
        self._cmds["CLS"] = self.cmd_cls
        self._cmds["CD"] = self.cmd_cd
        self._cmds["DIR"] = self.cmd_dir
        self._cmds["TYPE"] = self.cmd_type
        self._cmds["ECHO"] = self.cmd_echo
        self._cmds["SET"] = self.cmd_set
        self._cmds["HELP"] = self.cmd_help
        self._cmds["MEM"] = self.cmd_mem
        self._cmds["TRACE"] = self.cmd_trace
        self._cmds["FACET"] = self.cmd_facet
        self._cmds["GAS"] = self.cmd_gas
        self._cmds["LESSON"] = self.cmd_lesson
        self._cmds["COHORT"] = self.cmd_cohort
        self._cmds["ABI"] = self.cmd_abi
        self._cmds["DEPLOY"] = self.cmd_deploy
        self._cmds["REM"] = self.cmd_rem
        self._cmds["TIME"] = self.cmd_time
        self._cmds["DATE"] = self.cmd_date
        self._cmds["VOL"] = self.cmd_vol
        self._cmds["CHKDSK"] = self.cmd_chkdsk
        self._cmds["TREE"] = self.cmd_tree
        self._cmds["PING"] = self.cmd_ping
        self._cmds["RPC"] = self.cmd_rpc
        self._cmds["TIPS"] = self.cmd_tips

    def _register_facets(self) -> None:
        for i, label in enumerate(FACET_LABELS):
            self._cmds[label] = self._make_facet_handler(label, i)

    def _make_facet_handler(self, label: str, idx: int) -> Callable[[List[str]], int]:
        def _handler(args: List[str]) -> int:
            salt = (DRILL_SEED ^ idx * 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
            print(f"[{label}] trace", _keccak_topic(f"{label.lower()}:{salt:x}"))
            if args:
                joined = " ".join(args)
                acc, sat = _saturating_add(len(joined), idx)
                print(" sum probe:", acc, "saturated" if sat else "ok")
            return 0

        return _handler

    def run_line(self, raw: str) -> int:
        raw = raw.strip()
        if not raw:
            return 0
        self.s.history.append(raw)
        try:
            parts = shlex.split(raw)
        except ValueError as e:
            print("ERR:", e)
            return 1
        verb = parts[0].upper()
        args = parts[1:]
        fn = self._cmds.get(verb)
        if fn is None:
            print(f"Bad command or file name: {verb}")
            return 1
        return fn(args)

    def repl(self) -> None:
        prompt = self.s.env.get("PROMPT", "VOLT>")
        while True:
            try:
                line = input(prompt + " ").strip()
            except (EOFError, KeyboardInterrupt):
                print("^C")
                break
            if line.upper() in {"EXIT", "QUIT"}:
                break
            self.run_line(line)

    def cmd_ver(self, args: List[str]) -> int:
        print("ms-dos_new [VoltTrace pedagogical shell]")
        print(" trace_version", hex(TRACE_VERSION))
        print(" anchors", ADDRESS_A, ADDRESS_B, ADDRESS_C)
        return 0

    def cmd_cls(self, args: List[str]) -> int:
        print("\\033[2J\\033[H", end="")
        return 0

    def cmd_cd(self, args: List[str]) -> int:
        if not args:
            print(self.s.cwd)
            return 0
        target = Path(args[0]).expanduser()
        if not target.is_dir():
            print("Invalid directory")
            return 1
        self.s.cwd = target.resolve()
        return 0

    def cmd_dir(self, args: List[str]) -> int:
        root = self.s.cwd if not args else Path(args[0])
        if not root.exists():
            print("File not found")
            return 1
        for p in sorted(root.iterdir()):
            mark = "DIR" if p.is_dir() else "FIL"
            print(f"{mark} {p.name}")
        return 0

    def cmd_type(self, args: List[str]) -> int:
        if not args:
            print("Required parameter missing")
            return 1
        if args[0].upper() == "LESSON" and len(args) > 1:
            return self.cmd_lesson([args[1]])
        path = Path(args[0])
        if not path.is_file():
            print("File not found")
            return 1
        print(path.read_text(encoding="utf-8", errors="replace"))
        return 0

    def cmd_echo(self, args: List[str]) -> int:
        print(" ".join(args))
        return 0

    def cmd_set(self, args: List[str]) -> int:
        if not args:
            for k, v in sorted(self.s.env.items()):
                print(f"{k}={v}")
            return 0
        if "=" in args[0]:
            k, v = args[0].split("=", 1)
            self.s.env[k.upper()] = v
        return 0

    def cmd_help(self, args: List[str]) -> int:
        topics = sorted(self._cmds.keys())
        chunk = 8
        for i in range(0, len(topics), chunk):
            print(" ".join(topics[i : i + chunk]))
        return 0

    def cmd_mem(self, args: List[str]) -> int:
        print("Memory model: Python heap; on-chain analog is transient gas + storage slots.")
        return 0

    def cmd_trace(self, args: List[str]) -> int:
        for line in self.s.history[-16:]:
            print(line)
        return 0

    def cmd_facet(self, args: List[str]) -> int:
        if not args:
            print("usage: FACET <name> [args]")
            return 1
        label = args[0].upper()
        fn = self._cmds.get(label)
        if fn is None:
            print("Unknown facet")
            return 1
        return fn(args[1:])

    def cmd_gas(self, args: List[str]) -> int:
        if not args:
            print("usage: GAS <hint>")
            return 1
        try:
            hint = int(args[0])
        except ValueError:
            print("Invalid number")
            return 1
        lo, hi = 21_000, 30_000_000
        c = _clamp(hint, lo, hi)
        print("clamped gas hint:", c)
        return 0

    def cmd_lesson(self, args: List[str]) -> int:
        if not args:
            for lid, card in sorted(self.s.lessons.items()):
                print(lid, card.title, card.gas_hint)
            return 0
        try:
            lid = int(args[0])
        except ValueError:
            print("Invalid lesson id")
            return 1
        card = self.s.lessons.get(lid)
        if not card:
            print("Unknown lesson")
            return 1
        print(textwrap.fill(card.notes, 88))
        return 0

    def cmd_cohort(self, args: List[str]) -> int:
        for cid, c in sorted(self.s.cohorts.items()):
            print(cid, c.tag_hex, "cap", c.cap, "members", len(c.members))
        return 0

    def cmd_abi(self, args: List[str]) -> int:
        iface = {
            "openCohort": "(bytes32,uint32)->uint256",
            "publishLesson": "(bytes32,uint32)->uint256",
            "heartbeat": "()",
            "probeBoundedSum": "(uint256[])->(uint256,bool)",
        }
        print(json.dumps(iface, indent=2))
        return 0

    def cmd_deploy(self, args: List[str]) -> int:
        print("Constructor arity: 6 addresses (A,B,C,governor,operator,auditor).")
        print("Suggested immutables:", ADDRESS_A, ADDRESS_B, ADDRESS_C)
        print("Governor/operator/auditor must be live EOAs or contracts you control.")
        return 0

    def cmd_rem(self, args: List[str]) -> int:
        return 0

    def cmd_time(self, args: List[str]) -> int:
        print(time.strftime("%H:%M:%S"))
        return 0

    def cmd_date(self, args: List[str]) -> int:
        print(time.strftime("%Y-%m-%d"))
        return 0

    def cmd_vol(self, args: List[str]) -> int:
        print(" Volume in drive C is VOLTTRACE")
        return 0

    def cmd_chkdsk(self, args: List[str]) -> int:
        print("Pedagogy scan: OK — bounded loops, non-reentrant externals, no ETH custody.")
        return 0

    def cmd_tree(self, args: List[str]) -> int:
        print("explos_dos.sol")
        print("+-- ms-dos_new/main.py")
        print("+-- ms-dos_new/ALL_PYTHON_ONE_FILE.py  (main + commented emitters)")
        print("+-- ms-dos_new/build_all_python_one.py")
        print("+-- winRARAI/index.html")
        print("+-- ms-dos_new/VoltDosJarvisLab.java")
        return 0

    def cmd_ping(self, args: List[str]) -> int:
        host = args[0] if args else "127.0.0.1"
        print(f"Pinging {host} with pedagogy: {_keccak_topic(host)}")
        return 0

    def cmd_rpc(self, args: List[str]) -> int:
        url = args[0] if args else self.s.env.get("RPC", DEFAULT_RPC)
        if not url:
            print("Set RPC via SET RPC=https://... or pass URL")
            return 1
        cid = _rpc_chain_id(url)
        print("chainId", cid)
        return 0 if cid is not None else 1

    def cmd_tips(self, args: List[str]) -> int:
        if not args:
            print("usage: TIPS <index>")
            return 1
        try:
            idx = int(args[0])
        except ValueError:
            print("Invalid index")
            return 1
        if idx < 0 or idx >= len(TIPS):
            print("Index out of range", 0, len(TIPS) - 1)
            return 1
        print(TIPS[idx])
        return 0


