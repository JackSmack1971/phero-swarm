## Project Overview

This is a **Phero-Swarm AI agent coordination framework** that uses digital stigmergy (inspired by ant pheromone trails) to coordinate specialized AI agents through environmental modification rather than direct communication. The system transforms individual AI assistance into coordinated swarm intelligence for autonomous software development.

## Critical System Files - HANDLE WITH EXTREME CARE

### Primary Coordination Files
- **`.pheromone`** - THE COORDINATION NEXUS. This JSON file contains all coordination signals. NEVER write to it directly without using the PheromoneHandler class. Any corruption breaks the entire coordination system.
- **`.roomodes`** - Agent mode definitions. Modifications require system restart.
- **`.swarmConfig`** - Core swarm configuration. Contains signal categories and priorities.

### Core Python Modules
- **`src/traffic_controller.py`** - Routes tasks between agents based on pheromone signals
- **`src/pheromone_handler.py`** - Safe file operations for .pheromone (if created)
- **`docs/`** - All project documentation and blueprints
- **`templates/`** - Standard templates for specifications and architecture

## Development Guidelines

### Pheromone File Operations - CRITICAL SAFETY RULES

**NEVER do this:**
```python
# DON'T - This causes corruption
with open('.pheromone', 'w') as f:
    json.dump(data, f)
```

**ALWAYS do this:**
```python
# DO - Use atomic writes with validation
from pheromone_handler import PheromoneHandler
handler = PheromoneHandler()
handler.add_signal(signal_data)
```

### Signal Structure Standards
Every pheromone signal MUST have this exact structure:
```json
{
  "id": "unique-identifier-timestamp",
  "signalType": "descriptive_signal_type",
  "category": "compass|state|need|block|coordinate",
  "strength": 1.0-10.0,
  "target": "target_agent_slug",
  "message": "Human-readable description",
  "timestamp": 1640995200
}
```

### Agent Mode Guidelines

**Each agent mode MUST:**
1. Read `.pheromone` file at start of every task
2. Add completion signals when finishing work
3. Add handoff signals to route to next agent
4. Use `attempt_completion` with clear next steps
5. Handle pheromone file corruption gracefully

**File Access Patterns:**
- **Read-only agents**: `["read"]` - Can analyze but not modify
- **Implementation agents**: `["read", "edit"]` - Can modify source code
- **System agents**: `["read", ["edit", "\\.pheromone$"]]` - Can update coordination

### Code Quality Standards

**Function Guidelines:**
- Maximum 30 lines per function
- Use async/await for I/O operations
- Custom exceptions for error handling
- No hardcoded credentials or API keys
- Environment variables for configuration

**Testing Requirements:**
- Minimum 80% code coverage
- Tests must pass before any handoff
- Use pytest framework
- Test files in `tests/` directory

**File Organization:**
- Source code in `src/`
- Documentation in `docs/`
- Templates in `templates/`
- Tests in `tests/`
- Configuration files in project root

## Validation Instructions

### Before Any Code Changes
```bash
# 1. Validate pheromone file integrity
python -m json.tool .pheromone

# 2. Run existing tests
pytest tests/ -v

# 3. Check system configuration
python -c "import json; print('✅ Config valid' if json.load(open('.swarmConfig')) else '❌ Config invalid')"
```

### After Making Changes
```bash
# 1. Validate all JSON files
find . -name "*.json" -exec python -m json.tool {} \; > /dev/null

# 2. Run full test suite
pytest tests/ --cov=src/ --cov-report=term-missing

# 3. Test coordination system
python src/traffic_controller.py

# 4. Verify pheromone operations
python -c "
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
data = h.read_safe()
print('✅ Pheromone system healthy' if data else '❌ Pheromone corruption detected')
"
```

### Signal Validation
Before adding any signal to `.pheromone`:
```python
def validate_signal(signal):
    required_fields = ['id', 'signalType', 'category', 'strength', 'message']
    valid_categories = ['compass', 'state', 'need', 'block', 'coordinate']
    
    for field in required_fields:
        assert field in signal, f"Missing required field: {field}"
    
    assert signal['category'] in valid_categories, f"Invalid category: {signal['category']}"
    assert 0.0 <= signal['strength'] <= 10.0, f"Invalid strength: {signal['strength']}"
    assert len(signal['message']) > 0, "Message cannot be empty"
```

## Navigation and Context

### Project Structure
```
phero-swarm/
├── .pheromone          # Coordination signals (CRITICAL)
├── .roomodes           # Agent mode definitions
├── .swarmConfig        # System configuration
├── src/                # Core system code
│   ├── traffic_controller.py
│   └── pheromone_handler.py (if created)
├── docs/               # Project documentation
│   ├── *_Blueprint.md
│   └── architecture.md
├── templates/          # Standard templates
├── tests/              # Test suite
└── README.md
```

### Understanding the Coordination Flow
1. **Human** provides concept or task
2. **Traffic Controller** reads `.pheromone` and routes to appropriate agent
3. **Specialist Agent** completes task and adds completion signal
4. **System** automatically routes to next agent based on signals
5. **Coordination** continues until project completion

### Common Coordination Patterns
- `compass` signals → **concept-to-blueprint-translator**
- `need` + "test" → **tester-tdd-master**
- `need` + "architecture" → **architect-highlevel-module**
- `need` (general) → **coder-test-driven**
- `block` signals → **debugger-targeted**
- Unclear state → **orchestrator-pheromone-scribe**

## Work Presentation Standards

### Git Commit Messages
Follow this format:
```
[agent-slug] Brief description

- Specific change 1
- Specific change 2
- Pheromone signals added: signal_type_1, signal_type_2

Files modified:
- path/to/file1.py
- path/to/file2.md

Next agent: target-agent-slug
```

### Pull Request Guidelines
**Title Format:** `[Phase] Feature: Description`
**Description Must Include:**
- Agent coordination summary
- Pheromone signals timeline
- Testing verification
- Next steps for swarm

### Documentation Updates
- Update relevant `.md` files in `docs/`
- Add any new agent modes to `.roomodes`
- Document coordination patterns discovered
- Include failure scenarios and recovery procedures

## Emergency Procedures

### Pheromone File Corruption Recovery
```bash
# 1. Backup corrupted file
cp .pheromone .pheromone.corrupted

# 2. Create minimal valid structure
echo '{"signals": [], "metadata": {"created": '$(date +%s)'}}' > .pheromone

# 3. Validate
python -m json.tool .pheromone

# 4. Add initialization signal
python -c "
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
h.add_signal({
    'id': 'emergency-reset-' + str(int(time.time())),
    'signalType': 'system_recovery',
    'category': 'compass',
    'strength': 9.0,
    'message': 'Emergency recovery - system reset',
    'timestamp': int(time.time())
})
"
```

### Coordination Deadlock Recovery
```bash
# 1. Analyze current state
python src/traffic_controller.py

# 2. Check for stalled signals
python -c "
import json
data = json.load(open('.pheromone'))
signals = data.get('signals', [])
print(f'Active signals: {len(signals)}')
for s in signals[-3:]:
    print(f'{s.get(\"category\")}: {s.get(\"message\")}')
"

# 3. Clear stalled signals if needed
python -c "
from src.pheromone_handler import PheromoneHandler
h = PheromoneHandler()
h.clear_signals_by_category('coordinate')  # Clear old coordination
"

# 4. Route to orchestrator for analysis
# Switch to orchestrator-pheromone-scribe mode manually
```

### System Health Check
```bash
# Run this before starting any major work
python -c "
import json, os
print('🔍 System Health Check')
print('✅ .pheromone exists' if os.path.exists('.pheromone') else '❌ .pheromone missing')
try:
    json.load(open('.pheromone'))
    print('✅ .pheromone valid JSON')
except:
    print('❌ .pheromone corrupted')
print('✅ .roomodes exists' if os.path.exists('.roomodes') else '❌ .roomodes missing')
print('✅ .swarmConfig exists' if os.path.exists('.swarmConfig') else '❌ .swarmConfig missing')
"
```

## Agent-Specific Guidelines

### For Codex/OpenAI Models
- Always read this AGENTS.md file first
- Understand the pheromone coordination before making changes
- Use the validation procedures after any modifications
- Ask for clarification if coordination state is unclear
- Test thoroughly before handing off to next agent

### For Blueprint Generation
- Use `templates/Project_Blueprint_Template.md`
- Create comprehensive blueprints in `docs/` folder
- Add `compass` signal with blueprint location
- Signal `architect-highlevel-module` for next phase

### For Implementation
- Follow TDD principles strictly
- Keep functions under 30 lines
- Add completion signals to `.pheromone`
- Signal `tester-tdd-master` after implementation

### For Testing
- Require minimum 80% coverage
- Create test reports in `docs/test_report.md`
- Signal success/failure appropriately
- Route to `debugger-targeted` if tests fail

## Success Metrics

The system is working correctly when:
- ✅ `.pheromone` file remains valid JSON throughout workflow
- ✅ Agents autonomously hand off to next appropriate agent
- ✅ All tests pass with adequate coverage
- ✅ Documentation stays current with changes
- ✅ No manual intervention required for standard workflows
- ✅ System can recover gracefully from errors

## Remember: This is a Coordination System

The power of this system comes from **collective intelligence through environmental coordination**. Each agent contributes to the shared environment (pheromone trails) which guides the behavior of subsequent agents. Maintain this coordination discipline and the swarm will achieve complex goals autonomously.

**When in doubt**: Switch to `orchestrator-pheromone-scribe` mode to analyze coordination state and determine next steps.
