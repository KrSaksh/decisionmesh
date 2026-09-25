# DecisionMesh

> **Cost-aware decision infrastructure for autonomous AI agents.**

[![Status](https://img.shields.io/badge/status-early%20development-yellow.svg)](#current-status)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

DecisionMesh is an experimental decision and routing layer designed to select the most appropriate execution strategy for AI tasks.

Instead of sending every task to an expensive reasoning model, DecisionMesh evaluates incoming requests and dynamically routes them between lightweight models, stronger models, deterministic tools, or human review.

---

## Idea

```text
                          Task
                           |
                           v
                   +----------------+
                   |  DecisionMesh  |
                   | Decision Layer |
                   +-------+--------+
                           |
               +-----------+-----------+
               |           |           |
               v           v           v
           Cheap LLM   Strong LLM    Tool
```

---

## Goals

* **Reduce Costs:** Minimize unnecessary calls to high-cost reasoning models.
* **Maintain Performance:** Preserve high task-success rates across diverse agent workflows.
* **Traceability & Metrics:** Measure latency and inference cost in real time.
* **Smart Routing:** Provide confidence-aware routing and automated fallback mechanisms.
* **Policy Enforcement:** Support deterministic rule enforcement and safety constraints.
* **Benchmarking:** Measure dynamic routing efficiency against fixed-model baselines.

---

## Current Status

**Early Development**

The project is currently in the initial design and prototyping phase. API signatures and core routing logic are evolving rapidly.

---

## Architecture

DecisionMesh will progressively incorporate the following components:

- Task classification
- Decision routing engine
- Model adapters
- Deterministic tools integration
- Confidence-aware fallback
- Policy enforcement layer
- Benchmarking suite
- Observability & logging
- Load testing framework
- Docker deployment setup

---

## Research Question

> **Can a low-latency decision layer reduce AI inference cost and latency while maintaining task success compared with using a single large model for every task?**

---

## License

This project is licensed under the [MIT License](LICENSE).