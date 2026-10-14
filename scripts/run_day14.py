import csv
from collections import Counter
from pathlib import Path

from benchmarks.day14_tasks import build_tasks
from decisionmesh.decision import DecisionEngine
from decisionmesh.execution import Executor
from decisionmesh.features import FeatureExtractor
from decisionmesh.integration import IntegrationRunner
from decisionmesh.models.llm import CheapModel, StrongModel
from decisionmesh.policy import ConfidencePolicy, FallbackPolicy, PolicyEngine
from decisionmesh.router import DeterministicRouter
from decisionmesh.tools import Calculator

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "benchmarks" / "results"
OUTPUT_FILE = OUTPUT_DIR / "day14_results.csv"


def build_runner() -> IntegrationRunner:
    return IntegrationRunner(
        feature_extractor=FeatureExtractor(),
        decision_engine=DecisionEngine(DeterministicRouter()),
        policy_engine=PolicyEngine(
            confidence_policy=ConfidencePolicy(threshold=0.75),
            fallback_policy=FallbackPolicy(),
        ),
        executor=Executor(
            cheap_model=CheapModel(),
            strong_model=StrongModel(),
            calculator=Calculator(),
        ),
    )


def write_results(results) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "task_id",
        "task_type",
        "input",
        "input_length",
        "word_count",
        "has_math_expression",
        "has_code_indicators",
        "estimated_complexity",
        "initial_strategy",
        "final_strategy",
        "confidence",
        "success",
        "output",
        "latency_ms",
        "estimated_cost",
        "actual_cost",
        "error",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "task_id": result.task_id,
                    "task_type": result.task_type.value,
                    "input": result.input,
                    "input_length": result.features.input_length,
                    "word_count": result.features.word_count,
                    "has_math_expression": (
                        result.features.has_math_expression
                    ),
                    "has_code_indicators": (
                        result.features.has_code_indicators
                    ),
                    "estimated_complexity": (
                        result.features.estimated_complexity
                    ),
                    "initial_strategy": result.initial_strategy.value,
                    "final_strategy": result.final_strategy.value,
                    "confidence": result.confidence,
                    "success": result.success,
                    "output": result.output,
                    "latency_ms": result.latency_ms,
                    "estimated_cost": result.estimated_cost,
                    "actual_cost": result.actual_cost,
                    "error": result.error,
                }
            )


def print_report(results) -> None:
    total = len(results)
    successful = sum(result.success for result in results)
    failed = total - successful

    initial_counts = Counter(
        result.initial_strategy.value for result in results
    )
    final_counts = Counter(
        result.final_strategy.value for result in results
    )
    fallbacks = sum(
        result.initial_strategy != result.final_strategy
        for result in results
    )

    average_latency = (
        sum(result.latency_ms for result in results) / total
        if total
        else 0.0
    )
    estimated_cost = sum(result.estimated_cost for result in results)
    actual_cost = sum(result.actual_cost for result in results)

    print("\nDecisionMesh Day 14 Integration Run")
    print("=" * 40)
    print(f"Tasks:              {total}")
    print(f"Successful:         {successful}")
    print(f"Failed:             {failed}")
    print(
        f"Success rate:       {successful / total:.1%}"
        if total
        else "Success rate:       N/A"
    )
    print(f"Fallbacks:          {fallbacks}")
    print(f"Average latency:    {average_latency:.4f} ms")
    print(f"Estimated cost:     {estimated_cost:.4f}")
    print(f"Actual cost:        {actual_cost:.4f}")

    print("\nInitial strategies:")
    for strategy in sorted(initial_counts):
        print(f"  {strategy:<18} {initial_counts[strategy]}")

    print("\nFinal strategies:")
    for strategy in sorted(final_counts):
        print(f"  {strategy:<18} {final_counts[strategy]}")

    if failed:
        print("\nFailed tasks:")
        for result in results:
            if not result.success:
                print(f"  {result.task_id}: {result.error}")

    print(f"\nCSV report: {OUTPUT_FILE}")


def main() -> None:
    tasks = build_tasks()

    if not tasks:
        raise RuntimeError("The integration dataset is empty.")

    runner = build_runner()
    results = [runner.run(task) for task in tasks]

    write_results(results)
    print_report(results)


if __name__ == "__main__":
    main()
