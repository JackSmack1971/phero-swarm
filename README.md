# 🐜 Phero-Swarm: AI Agent Orchestration via Digital Stigmergy

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-2.3.1--simplified-brightgreen)

## 🌟 Overview

Phero-Swarm is an **AI agent swarm orchestration framework** based on **digital stigmergy** — inspired by how ants coordinate through pheromone trails. Agents communicate by modifying a shared `.pheromone` file rather than direct messaging, enabling emergent coordination patterns for software development tasks.

### 🧠 Key Concepts

- **Digital Stigmergy**: Agents coordinate by reading/writing signals to a shared `.pheromone` file
- **Signal-Based Routing**: A traffic controller routes tasks based on pheromone signal analysis
- **Specialized Agents**: Each agent has specific roles, file access permissions, and capabilities
- **Evaporating Signals**: Signals decay over time, keeping the system focused on current priorities
- **Human-Readable Communication**: All agent outputs are designed for human understanding

## 🏗️ Current Architecture

### Agent Types (Defined in `.ROOMODES`)

**🚦 Traffic & Coordination**
- `traffic-controller`: Routes tasks based on pheromone signals
- `orchestrator-pheromone-scribe`: Maintains the `.pheromone` file and coordinates handoffs

**📋 Planning & Architecture**  
- `concept-to-blueprint-translator`: Converts user concepts into project blueprints
- `blueprint-feasibility-validator`: Validates project blueprints for risks and constraints
- `research-planner-strategic`: Gathers information and plans follow-up tasks
- `architect-highlevel-module`: Designs high-level system architecture
- `architect-with-verification`: Architecture design with explicit verification and ADR tracking

**⚙️ Development & Testing**
- `coder-test-driven`: Implements features using TDD methodology
- `debugger-targeted`: Diagnoses and fixes reported issues
- `tester-tdd-master`: Runs automated tests and reports coverage
- `context-manager`: Preserves project context across agent handoffs

**🔍 Quality & Security**
- `security-validator`: Performs static/dynamic security analysis and threat modeling
- `performance-optimizer`: Profiles code and suggests optimizations  
- `code-quality-auditor`: Assesses architecture and maintainability

## 🧪 Pheromone System

The `.pheromone` file contains structured signals that coordinate agent behavior:

```json
{
  "signals": [
    {
      "id": "unique-signal-id",
      "signalType": "framework_scaffolding_needed",
      "target": "coder-test-driven", 
      "category": "need",
      "strength": 8.0,
      "message": "Framework scaffolding required",
      "context": {
        "modified_files": ["@docs/NewProject_Alpha_Blueprint.md"],
        "key_decisions": ["use fastapi"],
        "handoff_instructions": "generate project skeleton",
        "verification": {"tests_passed": false},
        "token_usage": 60,
        "complexity_score": 4
      }
    }
  ]
}
```

### Signal Categories
- **compass**: Strategic project direction (highest priority)
- **state**: Progress updates and completion status
- **need**: Work requests requiring agent action
- **block**: Problems or obstacles needing resolution
- **coordinate**: Agent handoffs and collaboration

## 🔄 How It Works

1. **Signal Generation**: Agents complete work and emit progress signals
2. **Traffic Control**: `traffic-controller` analyzes signals and routes to appropriate agents
3. **Intelligent Routing**: Uses context continuity, specialist routing, and load balancing
4. **Signal Evolution**: Signals evaporate over time, duplicates are consolidated
5. **Human Oversight**: Built-in quality gates and escalation triggers

## 🛠️ Current Implementation

### Core Python Modules

**`src/traffic_controller.py`**
- Intelligent agent routing based on signal analysis
- Context continuity (keeps agents on related tasks)
- Specialist routing (security issues → security-validator)
- Circuit breaker pattern (avoids overloaded agents)
- Load balancing across available agents

**`src/pheromone_helpers.py`**
- Core pheromone file operations (load/save)
- Signal strength calculation
- Context sanitization and compression
- Signal consolidation logic

**`src/signal_optimizer.py`**
- Signal deduplication and consolidation
- Strength normalization
- Adaptive evaporation (signals decay over time)
- Signal clustering by context

**`src/architecture_diagrams.py`**
- Generates Mermaid diagrams from current signals
- Visualizes signal flow and file dependencies
- Auto-updates `docs/architecture/` directory

**`src/context_manager.py`**
- Extracts decisions from agent summaries
- Compresses context to stay under token limits
- Validates file references for security
- Tracks progress between contexts

**`src/signal_analytics.py`**
- Signal pattern analysis and metrics
- Pollution detection (signal types exceeding thresholds)
- Performance tracking

### Configuration Files

**`.swarmConfig`**
- Core system configuration
- Signal categories and priorities
- Evaporation rates and thresholds
- Context management settings

**`.ROOMODES`**
- Agent role definitions and permissions
- File access patterns (regex-based)
- Allowed tools and groups
- Custom instructions for each agent

### Templates

- `templates/Project_Blueprint_Template.md`: Project planning structure
- `templates/Architecture_Design_Template.md`: System design documentation
- `templates/Feature_Specification_Template.md`: Feature requirements

### Validation & Health Scripts

**`scripts/validate_agent_access.py`**
- Validates agent permissions and file access patterns
- Security checks for disallowed tools
- Ensures proper group membership

**`scripts/architecture_health.py`**
- Counts TODO markers (technical debt)
- Analyzes Architecture Decision Records (ADRs)
- Updates architecture health signals

## 🚀 Getting Started

### Basic Usage

1. **Create a project blueprint** using `docs/NewProject_Alpha_Blueprint.md` as a template
2. **Initialize signals** by having the `concept-to-blueprint-translator` process your concept
3. **Let the swarm work**: The `traffic-controller` will automatically route tasks
4. **Monitor progress** by examining the `.pheromone` file and generated diagrams

### Example Signal Flow

```bash
# Generate architecture diagrams from current signals
python src/architecture_diagrams.py

# Validate agent permissions
python scripts/validate_agent_access.py

# Check architecture health
python scripts/architecture_health.py

# Run traffic controller to get next agent
python src/traffic_controller.py
```

## 🔧 Key Features

### Intelligent Traffic Control
- **Context Continuity**: Agents stay with related tasks
- **Specialist Routing**: Route security/performance issues to specialists  
- **Circuit Breaker**: Avoid agents with high failure rates
- **Load Balancing**: Distribute work evenly

### Signal Management
- **Adaptive Evaporation**: Signals decay based on category and urgency
- **Duplicate Consolidation**: Merge similar signals automatically
- **Strength Normalization**: Keep signal strengths in 0-10 range
- **Pattern Detection**: Learn from successful coordination sequences

### Security & Validation
- **File Access Control**: Regex-based file permission system
- **Tool Restrictions**: Whitelist of allowed tools per agent
- **Input Sanitization**: All inputs validated and sanitized
- **Permission Validation**: Scripts to verify agent access patterns

## 🧪 Testing

The system includes comprehensive tests for all core modules:

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Test specific modules
pytest tests/test_traffic_controller.py
pytest tests/test_pheromone_helpers.py
pytest tests/test_signal_optimizer.py
```

## 📈 Current Capabilities vs. Planned

**✅ Currently Implemented:**
- Core pheromone signaling system
- Intelligent traffic routing
- 14 specialized agent definitions
- Signal optimization and evaporation
- Security validation and access control
- Architecture diagram generation
- Comprehensive test suite

**🚧 Planned/Partially Implemented:**
- Full agent execution environment
- Human review integration workflows
- Advanced learning from feedback
- Multi-project coordination
- Extended performance monitoring

## 🤝 Contributing

We welcome contributions to enhance the Phero-Swarm framework:
- Improved routing algorithms
- Additional agent specializations
- Enhanced signal analytics
- Performance optimizations
- Security enhancements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Current Status**: Core coordination framework implemented with intelligent routing, signal management, and comprehensive testing. Ready for integration with agent execution environments.
