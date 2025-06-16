# Troubleshooting

This guide collects common fixes and diagnostic steps for the Phero-Swarm system.

## Common Issues and Solutions

### Pheromone File Corruption
1. Backup the corrupted file:
   ```bash
   cp .pheromone .pheromone.corrupted
   ```
2. Create a minimal valid structure:
   ```bash
   echo '{"signals": [], "metadata": {"created": '$(date +%s)'}}' > .pheromone
   ```
3. Validate the new file:
   ```bash
   python -m json.tool .pheromone
   ```
4. Add an initialization signal using `PheromoneHandler`:
   ```bash
   python - <<'PY'
from src.pheromone_handler import PheromoneHandler
import time
h = PheromoneHandler()
h.add_signal({
    'id': 'emergency-reset-' + str(int(time.time())),
    'signalType': 'system_recovery',
    'category': 'compass',
    'strength': 9.0,
    'message': 'Emergency recovery - system reset',
    'timestamp': int(time.time())
})
PY
   ```

### Coordination Deadlock
1. Inspect the current state:
   ```bash
   python src/traffic_controller.py
   ```
2. Check for stalled signals:
   ```bash
   python - <<'PY'
import json
signals = json.load(open('.pheromone')).get('signals', [])
print(f'Active signals: {len(signals)}')
for s in signals[-3:]:
    print(f"{s.get('category')}: {s.get('message')}")
PY
   ```
3. Clear old coordination signals if necessary:
   ```bash
   python - <<'PY'
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
h.clear_signals_by_category('coordinate')
PY
   ```

### Missing Configuration
Ensure `.ROOMODES` and `.swarmConfig` exist:
```bash
ls -1 .ROOMODES .swarmConfig
```
If either file is missing, restore it from version control and restart the system.

## Diagnostic Procedures
- Validate pheromone file integrity:
  ```bash
  python -m json.tool .pheromone
  ```
- Run health validation:
  ```bash
  python validate_system_health.py
  ```
- Inspect recent coordination activity:
  ```bash
  python coordination_monitor.py --once
  ```

## Recovery Protocols
Follow the steps above for specific issues. After recovery, run:
```bash
pytest tests/ --cov=src/ --cov-report=term-missing
python src/traffic_controller.py
```
This ensures the system is stable before resuming autonomous operation.

## System Health Check
Run this before major work:
```bash
python - <<'PY'
import json, os
print('🔍 System Health Check')
print('✅ .pheromone exists' if os.path.exists('.pheromone') else '❌ .pheromone missing')
try:
    json.load(open('.pheromone'))
    print('✅ .pheromone valid JSON')
except Exception:
    print('❌ .pheromone corrupted')
print('✅ .ROOMODES exists' if os.path.exists('.ROOMODES') else '❌ .ROOMODES missing')
print('✅ .swarmConfig exists' if os.path.exists('.swarmConfig') else '❌ .swarmConfig missing')
PY
```
