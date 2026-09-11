# 📚 AutomationFlow Documentation

This directory contains the project-level documentation needed to understand, configure, and present AutomationFlow.

## Documentation Map

### 🏗️ Architecture

Read [architecture/architecture.md](architecture/architecture.md) for the system design, workflow boundaries, integration flow, and implementation roles.

### ⚙️ Setup

Read [setup/setup.md](setup/setup.md) for the local setup and configuration process.

## Documentation Principles

The documentation separates the automation platforms from the supporting application layer so that the project remains clear to both technical reviewers and prospective clients.

```text
Business Requirement
        ↓
Workflow Architecture
        ↓
n8n / Make Implementation
        ↓
Optional Python Processing Layer
        ↓
Deployment & Configuration
```
