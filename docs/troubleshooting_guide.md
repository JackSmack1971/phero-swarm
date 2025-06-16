# Troubleshooting Guide

Use this guide to resolve common issues with the Phero-Swarm system.

## Diagnose Pheromone File
```bash
python diagnose_pheromone.py .pheromone
```

## Validate System Health
```bash
python validate_system_health.py
```

## Reset the System
```bash
python reset_phero_swarm.py
```

If problems persist, inspect recent signals using:
```bash
python coordination_monitor.py --once
```
