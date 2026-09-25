# DecisionMesh

> Cost-aware decision infrastructure for autonomous AI agents.

DecisionMesh is an experimental decision and routing layer designed to
select the most appropriate execution strategy for AI tasks.

Instead of sending every task to an expensive reasoning model, DecisionMesh
evaluates the task and chooses between lightweight models, stronger models,
deterministic tools, or human review.

## Core idea

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

## Project Goals
> Reduce unnecessary expensive-model calls
> Maintain high task-success rates
> Measure latency and inference cost
> Provide confidence-aware routing
> Support fallback and policy enforcement
> Benchmark routing against fixed-model baselines
> Current Status

## Early development

Planned Architecture

The project will progressively include:

> Task classification
> Decision routing
> Model adapters
> Deterministic tools
> Confidence-aware fallback
> Policy enforcement
> Benchmarking
> Observability
> Load testing
> Docker deployment
> Research Question

Can a low-latency decision layer reduce AI inference cost and latency
while maintaining task success compared with using a single large model
for every task?

License

MIT