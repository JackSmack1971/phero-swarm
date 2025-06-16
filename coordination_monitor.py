import argparse
import asyncio
import os
import time
from typing import Any, Dict, List

from src.pheromone_handler import PheromoneHandler, PheromoneHandlerError
from src.traffic_controller import analyze_signal


class MonitorError(Exception):
    """Raised when coordination monitoring fails."""


def detect_coordination_deadlock(signals: List[Dict[str, Any]], stall_sec: int) -> bool:
    """Return True if no activity or circular routing within stall_sec."""
    now = int(time.time())
    recent = [s for s in signals if now - s.get("timestamp", now) <= stall_sec]
    if not recent:
        return True
    targets = [s.get("target") for s in recent if s.get("category") == "coordinate"]
    return len(set(targets)) == 1 and len(targets) > 2


def analyze_signal_health(signals: List[Dict[str, Any]], expiry_sec: int) -> List[Dict[str, Any]]:
    """Return invalid or expired signals."""
    now = int(time.time())
    required = {"id", "signalType", "category", "strength", "message", "timestamp"}
    return [s for s in signals if not required.issubset(s) or now - s.get("timestamp", now) > expiry_sec]


def suggest_next_action(signals: List[Dict[str, Any]]) -> str:
    """Suggest next agent based on latest valid signal."""
    for sig in sorted(signals, key=lambda s: s.get("timestamp", 0), reverse=True):
        agent = analyze_signal(sig)
        if agent:
            return agent
    return "orchestrator-pheromone-scribe"


def cleanup_expired_signals(signals: List[Dict[str, Any]], expiry_sec: int) -> List[Dict[str, Any]]:
    """Return signals newer than expiry_sec."""
    now = int(time.time())
    return [s for s in signals if now - s.get("timestamp", now) <= expiry_sec]


class CoordinationMonitor:
    """Monitor pheromone file and maintain coordination health."""

    def __init__(self, path: str, stall_min: int, expiry_min: int) -> None:
        self.handler = PheromoneHandler(path)
        self.stall_sec = stall_min * 60
        self.expiry_sec = expiry_min * 60

    async def load_signals(self) -> List[Dict[str, Any]]:
        data = await self.handler.read_safe()
        return data.get("signals", []) if data else []

    async def reset_deadlock(self) -> None:
        await self.handler.clear_signals_by_category("coordinate")
        signal = {
            "id": f"reset-{int(time.time())}",
            "signalType": "auto_recovery",
            "category": "coordinate",
            "strength": 9.0,
            "target": "orchestrator-pheromone-scribe",
            "message": "Deadlock detected - routing to orchestrator",
            "timestamp": int(time.time()),
        }
        await self.handler.add_signal(signal)

    async def display_dashboard(self, signals: List[Dict[str, Any]]) -> None:
        by_cat: Dict[str, int] = {}
        for s in signals:
            by_cat[s.get("category", "unknown")] = by_cat.get(s.get("category", "unknown"), 0) + 1
        handoffs = [s for s in signals if s.get("category") == "coordinate"][-5:]
        state = suggest_next_action(signals)
        print("Active signals:", by_cat)
        print("Recent handoffs:", [h.get("target") for h in handoffs])
        print("Suggested next action:", state)

    async def check_once(self) -> None:
        try:
            signals = await self.load_signals()
        except PheromoneHandlerError as exc:
            raise MonitorError("Unable to read pheromone") from exc
        if detect_coordination_deadlock(signals, self.stall_sec):
            await self.reset_deadlock()
            signals = await self.load_signals()
        invalid = analyze_signal_health(signals, self.expiry_sec)
        if invalid:
            print(f"Removing {len(invalid)} expired/malformed signals")
        cleaned = cleanup_expired_signals(signals, self.expiry_sec)
        if len(cleaned) != len(signals):
            await self.handler.write_safe({"signals": cleaned})
        await self.display_dashboard(cleaned)

    async def monitor_loop(self) -> None:
        while True:
            await self.check_once()
            await asyncio.sleep(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor coordination health")
    parser.add_argument("--path", default=os.getenv("PHEROMONE_FILE", ".pheromone"))
    parser.add_argument("--stall-minutes", type=int, default=int(os.getenv("STALL_MINUTES", "5")))
    parser.add_argument("--expiry-minutes", type=int, default=int(os.getenv("EXPIRY_MINUTES", "30")))
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    monitor = CoordinationMonitor(args.path, args.stall_minutes, args.expiry_minutes)
    try:
        if args.once:
            asyncio.run(monitor.check_once())
        else:
            asyncio.run(monitor.monitor_loop())
    except MonitorError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
