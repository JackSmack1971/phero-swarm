# Maintenance

Routine maintenance keeps the Phero-Swarm system reliable.

## Regular System Health Checks
- Validate the pheromone file and configuration:
  ```bash
  python -m json.tool .pheromone
  python validate_system_health.py
  ```
- Run the automated test suite regularly:
  ```bash
  pytest tests/ --cov=src/ --cov-report=term-missing
  ```
- Execute `python src/traffic_controller.py` to ensure routing works.

## Signal Cleanup Procedures
- Stale coordination signals can accumulate. Clear them with:
  ```bash
  python - <<'PY'
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
h.clear_signals_by_category('coordinate')
PY
  ```
- Review the pheromone file for unusual growth and trim unnecessary data.

## Performance Monitoring
- Use `scripts/architecture_health.py` to monitor technical debt.
- Generate signal analytics:
  ```bash
  python src/signal_analytics.py
  ```
- Monitor coverage reports to detect untested modules.

## Configuration Updates
- Edit `.swarmConfig` or `.ROOMODES` only via version control.
- After changing configuration, restart any running agents.
- Document changes in `docs/ADRs/` when they affect architecture.
