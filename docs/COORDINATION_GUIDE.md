# Coordination Guide

This document explains how agents communicate and how to intervene when needed.

## Signal Flow Between Agents
Agents read the `.pheromone` file at the start of each task. When an agent finishes work it adds a completion signal and typically a handoff signal for the next agent. `traffic-controller` analyzes signals and routes tasks based on the latest context.

A typical flow:
1. `concept-to-blueprint-translator` creates planning signals.
2. `traffic-controller` assigns the blueprint to `coder-test-driven`.
3. After implementation, `tester-tdd-master` validates and reports coverage.
4. The cycle continues until signals evaporate.

## Manual Intervention
Manual intervention is rarely required, but is appropriate when:
- Signals are stalled for an extended period.
- The pheromone file becomes invalid.
- A new mode must be introduced immediately.

To intervene:
1. Inspect signals using `coordination_monitor.py --once`.
2. If necessary, clear problematic signals using `PheromoneHandler.clear_signals_by_category()`.
3. Restart `traffic-controller` to resume automated routing.

## Understanding the Pheromone File
Every signal has the following structure:
```json
{
  "id": "unique-identifier-timestamp",
  "signalType": "descriptive_signal_type",
  "category": "compass|state|need|block|coordinate",
  "strength": 1.0,
  "target": "target_agent_slug",
  "message": "Human-readable description",
  "timestamp": 1640995200
}
```
Signals with higher strength are prioritized. The `category` field guides routing decisions and determines evaporation rates.

## Best Practices for Mode Usage
- Modify `.ROOMODES` through version control and restart the system after changes.
- Give each agent only the file permissions it needs.
- Always use `PheromoneHandler` for pheromone modifications.
- Monitor signal decay to avoid stale coordination.
