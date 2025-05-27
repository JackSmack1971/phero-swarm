# 🐜 Phero-Swarm: AI Agent Orchestration via Digital Stigmergy

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-2.2.0--performance--enabled-brightgreen)

## 🌟 Overview

Phero-Swarm is a sophisticated **AI agent swarm orchestration framework** based on the principles of **digital stigmergy** — inspired by how social insects like ants coordinate through pheromone trails. This system enables autonomous software development through intelligent coordination of specialized AI agents without requiring direct agent-to-agent communication.

### 🧠 Key Concepts

- **Digital Stigmergy**: Agents communicate by modifying a shared environment (`.pheromone` file) rather than direct messaging
- **Natural Language Communication**: Agents provide human-readable summaries of their work
- **Central State Management**: Only the Pheromone Scribe interprets and updates the shared state
- **Human-Centric Design**: All outputs optimized for human understanding and oversight
- **Self-Optimization**: System monitors performance and evolves agent capabilities

## 🏗️ Architecture

### Three-Tier Information Flow

```
Worker Modes → Task Orchestrators → Pheromone Scribe → .pheromone File
     ↓              ↓                    ↓              ↓
NL Summaries → Synthesis → Interpretation → JSON Signals
```

#### 1️⃣ Worker Modes (Executors)
Specialized agents that perform specific tasks:
- `coder-test-driven`: Implements code using TDD methodology
- `tester-tdd-master`: Creates and runs tests
- `debugger-targeted`: Diagnoses and fixes issues
- `optimizer-module`: Improves performance
- `docs-writer-feature`: Creates documentation
- *And many more...*

#### 2️⃣ Task Orchestrators (Coordinators)
Higher-level agents that manage project phases:
- `orchestrator-project-initialization`: Sets up new projects
- `orchestrator-framework-scaffolding`: Creates boilerplate code
- `orchestrator-feature-implementation-tdd`: Manages development
- `orchestrator-cross-feature-integration`: Handles system integration
- `orchestrator-refinement-and-maintenance`: Manages change requests

#### 3️⃣ Meta-Orchestrators (Strategic)
Highest-level agents managing the entire system:
- `uber-orchestrator`: Routes tasks and manages coordination
- `orchestrator-pheromone-scribe`: Interprets summaries and updates state
- `metagenesis-orchestrator`: Evolves and improves agent capabilities
- `orchestrator-meta-alignment`: Ensures project alignment with goals
- `orchestrator-collective-intelligence`: Optimizes reasoning systems

## 🧪 Pheromone System

The `.pheromone` file serves as the **collective memory and coordination medium**:

```json
{
  "signals": [
    {
      "id": "unique_signal_identifier",
      "signalType": "signal_type",
      "target": "target_entity",
      "strength": 0.8,
      "message": "Human-readable description",
      "data": {
        "entity_specific_data": "values",
        "file_paths": [],
        "status_codes": ""
      },
      "timestamp": "ISO_timestamp"
    }
  ],
  "documentation_registry": {
    /* Tracks all project documents for human reference */
  },
  "bayesian_beliefs": {
    /* Probabilistic reasoning about project state */
  },
  "temporal_patterns": {
    /* Detected sequences and workflows */
  },
  "learned_patterns": {
    /* Knowledge derived from successful sequences */
  }
}
```

## 🔄 Information Flow Process

1. **Worker Execution**: Worker agents complete tasks and generate rich natural language summaries
2. **Orchestrator Synthesis**: Task orchestrators combine worker summaries into comprehensive reports
3. **Scribe Interpretation**: Pheromone Scribe converts narratives into structured JSON signals
4. **State Update**: Signals are stored in `.pheromone` file with appropriate lifecycle management
5. **Collective Intelligence**: System learns from patterns and optimizes future behavior
6. **Evolution Triggers**: Performance monitoring initiates agent improvements when needed

## ✨ Key Innovations

### 🧬 Performance-Driven Evolution
The MetaGenesis system can evolve and improve agent capabilities:
- Tracks performance metrics (completion times, success rates, resource usage)
- Identifies inefficient patterns and recurring failures
- Automatically rewrites agent instructions to improve performance
- Uses Proof-Carrying Prompts (PCP) for safe evolution

### 📊 Multi-Dimensional Intelligence
- **Bayesian Belief Networks**: Probabilistic reasoning about project success
- **Temporal Pattern Detection**: Recognizes recurring sequences and workflows
- **Stigmergic Learning**: Reinforces successful patterns over time
- **Emergent Behavior Analysis**: Detects complex system behaviors

### 👤 Human-Centric Design
- All outputs designed for human understanding
- Comprehensive documentation registry
- Natural language summaries at every level
- Audit trails for debugging and oversight

### 📦 Compressed State Management
- Signals evaporate over time (fade away)
- Related signals are consolidated
- Operational details are archived
- Only critical information is retained

## 🚀 Getting Started

### Project Initialization
1. Create a blueprint file following the structure in `docs/NewProject_Alpha_Blueprint.md`
2. Initialize the project with your blueprint
3. The system will automatically:
   - Research and plan the project
   - Create specifications and architecture
   - Develop a framework scaffold
   - Implement features with tests
   - Document the entire system

### Configuration
Key configuration files:
- `.swarmConfig`: Core configuration
- `.swarm/detailed.config.json`: Interpretation logic
- `.swarm/performance.config.json`: Performance monitoring
- `.swarm/intelligence.config.json`: Collective intelligence
- `.swarm/coordination.config.json`: Peer coordination

## 📝 Blueprint Creation

The quality of your project blueprint significantly impacts swarm performance. A good blueprint includes:

1. **Strategic Foundation**
   - Primary goals (3-5 maximum)
   - Critical constraints
   - Technology mandates
   - Priority features

2. **Swarm-Optimized Feature Breakdown**
   - Dependencies between features
   - Parallel work opportunities
   - Integration points
   - Success criteria

3. **Performance and Evolution Guidance**
   - Expected agent patterns
   - Evolution triggers
   - Success metrics baselines

4. **Human Oversight Points**
   - Required reviews
   - Quality gates
   - Escalation triggers

See `docs/NewProject_Alpha_Blueprint.md` for a detailed example.

## 🔍 System Monitoring

### Tracking Project Progress
The `.pheromone` file contains all information about:
- Current project state
- Completed work
- Pending tasks
- Issues and blockers
- Performance metrics

### Human Intervention
The system is designed for appropriate human oversight:
- Review documentation in the `documentation_registry`
- Monitor performance through signal analysis
- Intervene at predefined quality gates
- Provide guidance when requested

## 🛠️ Advanced Features

### Peer Coordination Protocol
Orchestrators can coordinate across boundaries:
- Handshake protocol for cross-domain work
- Boundary establishment for resource protection
- Consultation mechanism for complex decisions

### Collective Intelligence Management
The system optimizes its reasoning capabilities:
- Bayesian network optimization
- Temporal pattern refinement
- Learning system supervision

### Error Recovery
The system can detect and recover from errors:
- Agent operational limit handling
- Workflow blockage resolution
- External system failure management

## 🤝 Contributing

We welcome contributions to enhance the Phero-Swarm framework:
- Improved agent definitions
- Enhanced interpretation logic
- New orchestration patterns
- Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Directions

- Enhanced learning from human feedback
- Multi-project coordination capabilities
- Domain-specific agent specialization
- Extended performance monitoring metrics
- Integration with external CI/CD systems
