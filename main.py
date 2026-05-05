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

