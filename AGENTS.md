# 🐜 Phero-Swarm Agent Operational Guide

## Project Overview: Digital Stigmergy Coordination System

**CRITICAL UNDERSTANDING**: This is not a traditional codebase. You are working within a **digital stigmergy system** where agents coordinate through environmental modification (`.pheromone` file) rather than direct communication. Your role is specialized, and coordination happens through pheromone signals.

### Core Principles
- **Environmental Coordination**: All agent coordination happens via `.pheromone` file updates
- **Specialized Roles**: Each agent has focused responsibilities defined in `.ROOMODES`
- **Human-Readable Output**: All summaries and documentation must be comprehensible to humans
- **Security First**: All inputs must be validated; file system access is strictly controlled
- **Context Preservation**: Critical information must survive agent handoffs

---

## 🗂️ Repository Structure & Navigation

### Key Coordination Files
```
.pheromone              # Central coordination state (JSON) - READ FIRST
.swarmConfig           # System configuration and signal definitions  
.ROOMODES              # Agent role definitions and access controls
```

### Core System Components
```
src/
├── traffic_controller.py     # Routes tasks based on pheromone signals
├── context_manager.py        # Preserves context across agent handoffs
├── pheromone_helpers.py     # Signal creation and validation utilities
├── security_manager.py      # Input validation and access controls
└── performance_monitor.py    # System optimization and metrics

templates/
├── Project_Blueprint_Template.md        # New project structure guide
├── Feature_Specification_Template.md    # Detailed feature specs
└── Architecture_Design_Template.md      # System design documentation

docs/
├── NewProject_Alpha_Blueprint.md        # Blueprint creation guidance
├── blueprint-generator-system-prompt.md # Security-aware blueprint generation
└── [project_name]_blueprint.md         # Current project blueprint (if exists)

tests/
├── test_traffic_controller.py          # Core routing logic tests
└── integration/                        # End-to-end workflow tests
```

### Navigation Best Practices
- **Always read `.pheromone` first** to understand current system state
- **Check your role in `.ROOMODES`** to understand your access permissions
- **Review project blueprint** in `docs/` for project-specific context
- **Use @file_path syntax** for precise file references in summaries

---

## 🧪 Pheromone System Usage Guide

### Reading Pheromone Signals
```bash
# Always start by understanding current state
cat .pheromone | jq '.signals[] | select(.category == "need" or .category == "block")'
```

### Signal Categories & Meanings
- **compass**: Project-level guidance and blueprints (strength: 10.0)
- **state**: Completed work and system status (strength: 1.0-7.5)  
- **need**: Work requiring attention (strength: 5.0-8.0)
- **block**: Critical issues requiring immediate action (strength: 8.0-9.0)
- **coordinate**: Cross-agent handoff coordination (strength: 6.0-7.0)

### Creating Pheromone Updates
**REQUIRED FORMAT** for all agent summaries:
```python
# Use pheromone_helpers.py for updates (when available)
{
    "signalType": "specific_work_type",
    "category": "appropriate_category", 
    "strength": calculated_priority,
    "message": "Human-readable summary of work completed",
    "context": {
        "modified_files": ["list", "of", "files"],
        "key_decisions": ["important", "choices", "made"],
        "handoff_instructions": "specific guidance for next agent",
        "complexity_score": 1-10
    }
}
```

### Context Preservation Requirements
- **File References**: Use exact paths with @mentions: `@src/traffic_controller.py`
- **Decision Documentation**: Record WHY choices were made, not just WHAT was done
- **Handoff Context**: Provide specific, actionable guidance for the next agent
- **Token Awareness**: Keep context summaries under 500 tokens while preserving critical information

---

## 🎭 Agent Role Adherence & Specialization

### Understanding Your Role
1. **Check `.ROOMODES`** for your specific agent definition
2. **Respect access controls**: Only modify files matching your `fileRegex` patterns
3. **Stay within tool groups**: Use only the tools granted to your role
4. **Follow custom instructions**: Your role's specific methodology and constraints

### Common Agent Types & Responsibilities

#### Orchestrators (Coordinators)
- **traffic-controller**: Route tasks based on pheromone analysis
- **orchestrator-pheromone-scribe**: Interpret summaries and update state
- **orchestrator-meta-alignment**: Ensure project alignment with goals

#### Specialists (Executors)  
- **coder-test-driven**: Implement features using TDD (max 30 lines per function)
- **tester-tdd-master**: Create and run comprehensive tests (80% coverage minimum)
- **debugger-targeted**: Diagnose and fix specific issues
- **security-validator**: SAST/DAST scanning and threat modeling
- **performance-optimizer**: Profiling and optimization recommendations

#### Support (Documentation & Context)
- **architect-highlevel-module**: System design and architecture decisions
- **docs-writer-feature**: Technical documentation and API specs
- **context-manager**: Maintain context across agent transitions

### Role Transition Protocol
When your work is complete:
1. **Summarize work** in human-readable format
2. **Update pheromone signals** with context and handoff instructions
3. **Validate your changes** according to your role's requirements
4. **Do not assume next agent** - let traffic-controller route appropriately

---

## 🔒 Security Requirements & Procedures

### Input Validation (MANDATORY)
- **All external inputs** must be validated against schemas before processing
- **Pheromone updates** must be sanitized to prevent injection attacks
- **Blueprint data** must follow sanitization procedures from `docs/blueprint-generator-system-prompt.md`
- **Configuration changes** require schema validation and audit logging

### File System Access Controls
- **Respect fileRegex patterns** defined in your `.ROOMODES` role
- **Minimum privilege principle**: Only access files necessary for your specific task
- **No privilege escalation**: Don't attempt to access files outside your permissions
- **Audit trail**: All file modifications must be logged in pheromone updates

### Authentication & Integrity
- **Agent identity verification** required for peer coordination
- **Pheromone file integrity** must be maintained (checksums/signatures)
- **Configuration file validation** against strict schemas
- **Secure handoff protocols** for sensitive operations

### Security Escalation
**Immediately create BLOCK signal** for:
- Security vulnerabilities discovered in code
- Potential privilege escalation attempts
- Input validation failures
- Suspicious pheromone signal patterns

---

## ⚙️ Development Workflow & Testing

### Code Implementation Standards
```python
# Required patterns for all code:
# 1. Functions max 30 lines
async def process_data(input_data: dict) -> dict:
    """Process data with comprehensive error handling."""
    try:
        # Implementation here (max 30 lines)
        return result
    except ValidationError as e:
        raise CustomValidationError(f"Invalid input: {e}") from e

# 2. Async I/O for all external operations
async def load_config() -> dict:
    return await asyncio.to_thread(json.loads, Path(".swarmConfig").read_text())

# 3. Custom exceptions for error handling
class PheromoneValidationError(Exception):
    """Raised when pheromone signal validation fails."""
```

### Testing Requirements
- **Unit tests required** for all new functionality
- **Minimum 80% code coverage** (enforced by `tester-tdd-master`)
- **Integration tests** for agent coordination workflows
- **Security tests** for input validation and access controls

### Test Execution
```bash
# Run tests before creating pheromone updates
pytest tests/ --cov=src --cov-report=term-missing
# Coverage must be ≥80% for completion signal
```

### Quality Gates
1. **Code Quality**: All linting and type checking must pass
2. **Test Coverage**: Minimum 80% coverage maintained
3. **Security Scan**: No critical security findings
4. **Performance**: No regression beyond 10% of baseline

---

## 📋 Work Validation & Review Processes

### Pre-Completion Checklist
**Before updating pheromone with completion signals**:
- [ ] All tests pass (`pytest tests/`)
- [ ] Code quality checks pass (`flake8`, `mypy`)
- [ ] Security validation complete (input sanitization verified)
- [ ] Documentation updated (docstrings, README sections)
- [ ] Context preserved for next agent (handoff instructions clear)
- [ ] File access stayed within role permissions

### Human Oversight Triggers
**Create `human_review_requested` signal** when:
- Architecture decisions affect multiple system components
- Security changes require compliance validation
- Performance changes exceed established baselines
- Complex debugging requires domain expertise
- Cross-team coordination needed

### Review Documentation
All major work must include:
- **Decision Record**: Why specific approaches were chosen
- **Impact Analysis**: What other components might be affected
- **Risk Assessment**: Potential issues and mitigation strategies
- **Next Steps**: Clear guidance for continuation

---

## 🔄 Common Workflow Patterns

### Starting Work (Any Agent)
1. **Read current state**: `cat .pheromone | jq '.signals'`
2. **Check your role**: Review `.ROOMODES` for your specific permissions
3. **Load project context**: Read relevant blueprint and architecture docs
4. **Validate prerequisites**: Ensure dependencies are met

### Blueprint-Driven Development
```bash
# For new projects, always start with blueprint
# 1. concept-to-blueprint-translator creates blueprint
# 2. architect-highlevel-module designs system
# 3. coder-test-driven implements features
# 4. tester-tdd-master validates implementation
```

### Issue Resolution Pattern
```bash
# For bugs and blocks:
# 1. debugger-targeted analyzes the problem
# 2. Specialist agents (security, performance) provide expertise
# 3. coder-test-driven implements fixes
# 4. tester-tdd-master validates resolution
```

### Context Handoff Pattern
```markdown
## Agent Handoff Summary
**Work Completed**: [Specific accomplishments]
**Files Modified**: @src/file1.py, @docs/file2.md
**Key Decisions**: [Important choices made and rationale]
**Next Agent Context**: [Specific guidance for continuation]
**Verification Status**: [Tests passed, security validated, etc.]
```

---

## 🚨 Troubleshooting & Error Recovery

### Common Issues & Solutions

#### Pheromone Signal Pollution
**Symptoms**: Too many low-strength signals, unclear routing
**Solution**: Use signal consolidation patterns, increase strength thresholds

#### Context Loss Between Agents
**Symptoms**: Repeated work, missing context, unclear handoffs
**Solution**: Enhance handoff instructions, use @file_path references

#### Infinite Agent Loops
**Symptoms**: Same signals repeating, no progress
**Solution**: Add circuit breaker logic, escalate to human review

#### Permission/Access Errors
**Symptoms**: File access denied, tool restrictions
**Solution**: Verify role permissions in `.ROOMODES`, use appropriate agent type

### Escalation Procedures
1. **Technical Issues**: Create BLOCK signal with specific error details
2. **Security Concerns**: Immediate BLOCK signal + human review request
3. **Architecture Questions**: Route to `architect-highlevel-module`
4. **Performance Problems**: Route to `performance-optimizer`

### Emergency Procedures
**System-Level Issues**:
- Backup `.pheromone` file before major changes
- Validate all configuration changes against schemas
- Escalate immediately for security violations
- Request human intervention for architectural decisions

---

## 📊 Performance & Optimization Guidelines

### Token Usage Optimization
- **Context Compression**: Keep summaries under 500 tokens while preserving critical info
- **Selective File Loading**: Only load files directly relevant to your task
- **Efficient Pheromone Updates**: Consolidate related signals when possible

### Performance Baselines
- **Code Implementation**: < 45 minutes per feature component
- **Test Creation**: < 20 minutes per test suite  
- **Documentation**: < 15 minutes per API endpoint
- **Integration**: < 30 minutes per feature pair

### Optimization Triggers
**Escalate to performance-optimizer when**:
- Task completion time exceeds baseline by 50%
- Memory usage grows beyond expected patterns
- Test execution time increases significantly
- Pheromone file size grows beyond manageable limits

---

## 🎯 Success Metrics & Quality Standards

### Completion Criteria
**Work is considered complete when**:
- All tests pass with ≥80% coverage
- Security validation confirms no critical issues
- Documentation is updated and human-readable
- Context is preserved for next agent handoff
- Pheromone signals accurately reflect system state

### Quality Indicators
- **Code Quality**: Clean, well-documented, following project patterns
- **Test Quality**: Comprehensive coverage, meaningful assertions
- **Documentation Quality**: Clear, accurate, useful for humans
- **Context Quality**: Next agent can continue work without confusion

### System Health Metrics
- Signal processing efficiency (signals resolved vs. created)
- Agent specialization effectiveness (tasks completed successfully)
- Context preservation quality (handoff success rate)
- Human intervention frequency (lower is better for routine tasks)

---

## 🔧 Quick Reference Commands

```bash
# Essential operations for any agent

# Read current pheromone state
cat .pheromone | jq '.signals[] | select(.strength > 5.0)'

# Check system configuration  
cat .swarmConfig | jq '.signalCategories'

# Your agent role and permissions
cat .ROOMODES | jq '.customModes[] | select(.slug == "your-agent-name")'

# Run tests before completion
pytest tests/ --cov=src --cov-report=term-missing

# Validate JSON files
python -m json.tool .pheromone > /dev/null && echo "Valid"

# Check for security patterns
grep -r "TODO\|FIXME\|XXX\|HACK" src/ docs/
```

---

## 📚 Learning Resources

### Key Documentation
- `README.md`: System overview and core concepts
- `docs/NewProject_Alpha_Blueprint.md`: Blueprint creation patterns
- `templates/`: Standard templates for different work types
- `assessment`: Deep analysis of system capabilities and enhancement opportunities

### Understanding Digital Stigmergy
- Agents communicate through environment modification, not direct messaging
- Pheromone signals create coordination patterns that emerge naturally
- Context preservation enables complex multi-agent workflows
- Human oversight maintains quality and handles edge cases

### Best Practices Evolved From Real Usage
- Always preserve context for the next agent
- Validate all inputs and outputs according to security requirements
- Stay within your specialized role for maximum system efficiency
- Document decisions and rationale, not just implementation details
- Escalate appropriately rather than attempting work outside your expertise

---

**Remember**: You are part of an intelligent swarm system. Your individual excellence contributes to collective intelligence, but coordination through the pheromone system is what makes the swarm truly powerful. Work with precision, document thoroughly, and trust the system to route work appropriately.
