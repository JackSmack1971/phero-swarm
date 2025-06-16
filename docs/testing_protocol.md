# Testing Protocol

Follow these steps to validate the Phero-Swarm system:

1. **Validate JSON files**
   ```bash
   find . -name "*.json" -exec python -m json.tool {} \; > /dev/null
   ```
2. **Run the full test suite with coverage**
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```
3. **Run system health validation**
   ```bash
   python validate_system_health.py
   ```
4. **Check coordination monitor**
   ```bash
   python coordination_monitor.py --once
   ```

All tests must pass with at least 80% coverage before deployment.
