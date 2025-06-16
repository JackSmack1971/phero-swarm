# 🐜 Phero-Swarm: AI Agent Orchestration via Digital Stigmergy

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-2.2.1--security--hardened-brightgreen)

## 🌟 Overview

Phero-Swarm is a sophisticated **AI agent swarm orchestration framework** based on the principles of **digital stigmergy** — inspired by how social insects like ants coordinate through pheromone trails. This system enables autonomous software development through intelligent coordination of specialized AI agents without requiring direct agent-to-agent communication.

**Security Note**: The security of the Phero-Swarm system is paramount. All configurations must be validated against a schema before loading, and their storage and modification must be strictly controlled. Operational security measures, such as hardening execution environments and implementing robust monitoring, are critical.

### 🧠 Key Concepts

- **Digital Stigmergy**: Agents communicate by modifying a shared environment (`.pheromone` file) rather than direct messaging.
- **Natural Language Communication**: Agents provide human-readable summaries of their work.
- **Central State Management**: Only the Pheromone Scribe interprets and updates the shared state. The Pheromone Scribe's execution environment must be hardened and secured.
- **Human-Centric Design**: All outputs optimized for human understanding and oversight.
- **Self-Optimization**: System monitors performance and evolves agent capabilities.

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
- `orchestrator-refinement-and-maintenance`: Manages change requests

#### 3️⃣ Meta-Orchestrators (Strategic)
Highest-level agents managing the entire system:
- `traffic-controller`: Routes tasks based on pheromone signals
- `orchestrator-pheromone-scribe`: Interprets summaries and updates state. Its operational environment must be highly secure.
- `orchestrator-meta-alignment`: Ensures project alignment with goals.
- `orchestrator-collective-intelligence`: Optimizes reasoning systems.

## 🧪 Pheromone System

The `.pheromone` file serves as the **collective memory and coordination medium**.
**Security Note**: The `.pheromone` file is critical system state. Its integrity must be protected through strict file system permissions (write access only for the authenticated Pheromone Scribe process) and mechanisms like checksums or digital signatures to detect tampering.

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

1.  **Worker Execution**: Worker agents complete tasks and generate rich natural language summaries.
2.  **Orchestrator Synthesis**: Task orchestrators combine worker summaries into comprehensive reports.
3.  **Scribe Interpretation**: Pheromone Scribe converts narratives into structured JSON signals. This process must be robust against malformed or malicious inputs.
4.  **State Update**: Signals are stored in `.pheromone` file with appropriate lifecycle management.
5.  **Collective Intelligence**: System learns from patterns and optimizes future behavior. Inputs to this system must be validated.
6.  **Evolution Triggers**: Performance monitoring initiates agent improvements when needed. Data feeding evolution triggers must be secure and authentic.

## ✨ Key Innovations

### 🧬 Performance-Driven Evolution
The system can evolve and improve agent capabilities:
- Tracks performance metrics (completion times, success rates, resource usage). **Security**: These metrics must be sourced reliably and protected from tampering.
- Identifies inefficient patterns and recurring failures.
- Automatically rewrites agent instructions to improve performance. **Security**: The inputs influencing this rewriting (e.g., performance data, existing instructions) must be validated to prevent unsafe evolution.
- Uses **Proof-Carrying Prompts (PCP)** for safe evolution. PCP involves rigorous validation of inputs that guide evolution, ensuring that generated prompts are not only effective but also adhere to predefined safety constraints and do not introduce vulnerabilities. This includes checks against adversarial inputs and ensuring the semantic integrity of the evolved instructions.

### 📊 Multi-Dimensional Intelligence
- **Bayesian Belief Networks**: Probabilistic reasoning about project success.
- **Temporal Pattern Detection**: Recognizes recurring sequences and workflows.
- **Stigmergic Learning**: Reinforces successful patterns over time.
- **Emergent Behavior Analysis**: Detects complex system behaviors.

### 👤 Human-Centric Design
- All outputs designed for human understanding.
- Comprehensive documentation registry.
- Natural language summaries at every level.
- Audit trails for debugging and oversight.

### 📦 Compressed State Management
- Signals evaporate over time (fade away).
- Related signals are consolidated.
- Operational details are archived.
- Only critical information is retained.

## 🚀 Getting Started

### Project Initialization
1.  Create a blueprint file following the structure in `docs/NewProject_Alpha_Blueprint.md`. Ensure all inputs are sanitized.
2.  Initialize the project with your blueprint.
3.  The system will automatically:
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

**Security Note**: All JSON configuration files MUST be validated against a strict schema before being loaded by the system. Ensure these files are stored securely and changes are managed through a version control system with appropriate reviews.

## 📝 Blueprint Creation

The quality of your project blueprint significantly impacts swarm performance. A good blueprint includes:

1.  **Strategic Foundation**
    - Primary goals (3-5 maximum)
    - Critical constraints
    - Technology mandates
    - Priority features

2.  **Swarm-Optimized Feature Breakdown**
    - Dependencies between features
    - Parallel work opportunities
    - Integration points
    - Success criteria

3.  **Performance and Evolution Guidance**
    - Expected agent patterns
    - Evolution triggers
    - Success metrics baselines

4.  **Human Oversight Points**
    - Required reviews
    - Quality gates
    - Escalation triggers

See `docs/NewProject_Alpha_Blueprint.md` for a detailed example. The generation of blueprints from user concepts must follow strict input sanitization and validation procedures as outlined in `docs/blueprint-generator-system-prompt.md`.

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
Orchestrators can coordinate across boundaries. **Security**: This coordination is now protected by cryptographic agent authentication.
- **Authenticated Handshake Protocol**: Establishes secure communication channels based on verified agent identities.
- Boundary establishment for resource protection.
- **Authenticated Consultation Mechanism**: Ensures complex decisions are made with trusted parties.

### Collective Intelligence Management
The system optimizes its reasoning capabilities:
- Bayesian network optimization.
- Temporal pattern refinement.
- Learning system supervision.

### Error Recovery
The system can detect and recover from errors:
- Agent operational limit handling.
- Workflow blockage resolution.
- External system failure management.

## 🤝 Contributing

We welcome contributions to enhance the Phero-Swarm framework:
- Improved agent definitions
- Enhanced interpretation logic
- New orchestration patterns
- Performance optimizations
- Security enhancements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Directions

- Enhanced learning from human feedback
- Multi-project coordination capabilities
- Domain-specific agent specialization
- Extended performance monitoring metrics
- Integration with external CI/CD systems
