# AGENTS.md - Phero-Swarm AI Agent Orchestration Framework

## Project Overview

**What This Project Is**: A sophisticated AI agent coordination system based on digital stigmergy (inspired by ant pheromone trails). Agents communicate through a shared `.pheromone` file rather than direct messaging, enabling emergent collective intelligence for software development.

**Core Innovation**: Instead of agents talking to each other, they leave "chemical signals" in a shared environment that other agents can detect and respond to. This creates natural workflow coordination without complex orchestration logic.

**Current Challenge**: The system has grown overly complex with theoretical AI enhancements that don't map to real capabilities. We need to simplify while preserving the core stigmergic coordination innovation.

## Architecture Understanding

### Key Files and Their Purposes
- **`.ROOMODES`**: Defines specialized AI agent modes (currently over-engineered, needs simplification)
- **`.pheromone`**: The coordination hub - JSON file where agents leave status signals
- **`.swarmConfig`**: System configuration (currently has unrealistic AI enhancement claims)
- **`templates/`**: Project templates for agents to follow
- **`docs/`**: Documentation including blueprint examples

### How Coordination Actually Works
1. **Agent reads `.pheromone`** to understand current project state
2. **Agent performs specialized work** (coding, testing, documentation, etc.)
3. **Agent writes summary to `.pheromone`** describing what was accomplished
4. **Other agents detect these signals** and coordinate their work accordingly
5. **Human oversight** through clear documentation and review points

## Current Problems to Solve

### 1. Mode Definition Bloat
The `.ROOMODES` file has agents with 500+ word instructions full of security theater and non-existent AI capabilities. Each mode should have:
- **Single clear responsibility** 
- **Under 200 words of instructions**
- **Realistic capabilities only**
- **Clear input/output specifications**

### 2. Signal Taxonomy Chaos  
16+ signal types create coordination paralysis. Simplify to 5 core types:
- `compass`: Project guidance and goals
- `state`: Work completed notifications  
- `need`: Work required signals
- `block`: Workflow blockers
- `coordinate`: Agent handoff requirements

### 3. Unrealistic AI Claims
Remove references to neural networks, genetic algorithms, and predictive models that don't exist in this context. Focus on what's actually possible:
- Pattern detection in work sequences
- Performance monitoring and optimization
- Adaptive signal prioritization
- State persistence across sessions

## Development Guidelines

### When Working on .ROOMODES
- **Keep it simple**: Each agent should do ONE thing well
- **Remove security theater**: Focus on workflow coordination, not security frameworks
- **Practical tools only**: Most agents need only `["read"]` or `["read", "edit"]` access
- **Clear boundaries**: No overlapping responsibilities between agents

### When Updating .swarmConfig  
- **Signal simplicity**: Use only the 5 core signal types
- **Remove AI bloat**: Delete references to neural networks, genetic algorithms, etc.
- **Focus on coordination**: Configuration should enable better agent handoffs
- **Human oversight**: Maintain clear points for human review and intervention

### When Modifying .pheromone Structure
- **Readability first**: Humans need to understand the project state easily
- **Actionable signals**: Each signal should trigger clear next actions
- **State compression**: Keep file size manageable while preserving key information
- **Audit trail**: Maintain enough history for debugging coordination issues

## Testing Strategy

### Validation Approach
1. **Start simple**: Test with a basic web application blueprint
2. **Agent coordination**: Verify clean handoffs between specialized agents  
3. **Signal clarity**: Ensure `.pheromone` updates are human-readable
4. **No conflicts**: Confirm agents don't step on each other's work
5. **Human oversight**: Test review and intervention points

### Success Criteria
- Agents activate only when needed
- Clear workflow progression through project phases
- Human can understand project status from `.pheromone` file
- No coordination deadlocks or conflicts
- Practical development velocity improvements

## Code Quality Standards

### For Phero-Swarm Components
- **Simplicity over cleverness**: Prefer clear, simple coordination logic
- **JSON validation**: Ensure all config files are valid and parseable
- **Documentation sync**: Keep docs aligned with actual capabilities
- **Template consistency**: Ensure templates match agent capabilities

### For Generated Code
- **Follow project blueprints**: Respect the architectural decisions in blueprints
- **Test-driven development**: Include comprehensive tests with implementations
- **Documentation**: Generate clear README files and API documentation
- **Security basics**: Follow standard security practices without theater

## Common Patterns to Apply

### Effective Agent Coordination
```
1. Read .pheromone to understand current project state
2. Identify your specific contribution based on role
3. Complete focused work using available tools
4. Update .pheromone with clear, human-readable summary
5. Hand off to next appropriate agent if needed
```

### Blueprint-Driven Development
- Use `docs/NewProject_Alpha_Blueprint.md` as the template for new projects
- Ensure all development follows the blueprint's technical constraints
- Maintain clear feature dependency mapping for parallel work
- Include human review points at logical milestones

### Quality Maintenance
- Prioritize working code over perfect code
- Include tests with every implementation
- Document decisions and trade-offs clearly
- Maintain clean, readable codebases

## Tool Usage Guidelines

### File Operations
- Always use absolute paths when possible
- Read `.pheromone` before making major changes
- Update documentation when changing system behavior
- Maintain backup of critical configuration files

### External Integrations
- Be cautious with MCP tool usage - verify capabilities exist
- Focus on proven, stable integrations over experimental ones
- Document any external dependencies clearly
- Provide fallback options when external tools fail

## Success Metrics

### System Health Indicators
- Clean agent handoffs without conflicts
- Readable and actionable `.pheromone` state
- Steady progress through development phases
- Human comprehension of system state
- Practical development acceleration

### Warning Signs
- Agents conflicting over responsibilities
- `.pheromone` file becoming unreadable
- Coordination deadlocks or infinite loops
- Human confusion about project status
- System complexity increasing without clear benefits

---

**Remember**: This is an innovative coordination system, not an AI research project. Focus on making the stigmergic coordination work practically and elegantly. The magic is in simple agents creating complex collective behavior, not in individual agent sophistication.
