# Operational Checklists

Use these checklists to keep the swarm running smoothly.

## Daily System Health Verification
- [ ] Validate `.pheromone` with `python -m json.tool .pheromone`
- [ ] Run `python validate_system_health.py`
- [ ] Execute `pytest tests/ -q` to catch regressions
- [ ] Review recent signals via `coordination_monitor.py --once`

## Recovery from Coordination Failures
1. Check active signals:
   ```bash
   python src/traffic_controller.py
   ```
2. Identify stalled or conflicting signals.
3. Clear obsolete coordination signals:
   ```bash
   python - <<'PY'
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
h.clear_signals_by_category('coordinate')
PY
   ```
4. Restart the swarm with `python src/traffic_controller.py`.

## Adding New Modes Safely
- [ ] Update `.ROOMODES` with the new mode definition.
- [ ] Commit the change to version control.
- [ ] Restart all running agents to load the new mode.
- [ ] Monitor for unexpected behavior using `coordination_monitor.py`.

## Project Initialization Best Practices
- [ ] Start from `templates/Project_Blueprint_Template.md`.
- [ ] Generate architecture diagrams with `src/architecture_diagrams.py`.
- [ ] Ensure initial signals include clear handoff instructions.
- [ ] Document configuration decisions in `docs/ADRs/`.
