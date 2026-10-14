
from decisionmesh.models import Task, TaskType


def build_tasks() -> list[Task]:
    """Build a deterministic dataset containing 100 tasks."""

    tasks: list[Task] = []

    # 20 arithmetic tasks.
    for i in range(20):
        tasks.append(
            Task(
                id=f"math-{i:03d}",
                input=f"{i} + {i + 2} * 3",
                task_type=TaskType.MATH,
                complexity=0.1,
            )
        )

    # 20 easy general tasks.
    easy_prompts = [
        "Say hello.",
        "Define a variable.",
        "Explain a loop.",
        "Name a data type.",
        "Define an API.",
    ]

    for i in range(20):
        tasks.append(
            Task(
                id=f"easy-{i:03d}",
                input=f"{easy_prompts[i % len(easy_prompts)]} Variant {i}.",
                task_type=TaskType.GENERAL,
                complexity=0.2,
            )
        )

    # 20 higher-complexity general tasks.
    hard_prompts = [
        "Explain the tradeoffs between consistency and availability in a distributed system.",
        "Describe how a database index affects reads, writes, and storage.",
        "Explain how retries and timeouts interact in a distributed service.",
        "Compare synchronous and asynchronous communication between services.",
        "Describe a strategy for debugging a high-latency backend API.",
    ]

    for i in range(20):
        tasks.append(
            Task(
                id=f"hard-{i:03d}",
                input=(
                    f"{hard_prompts[i % len(hard_prompts)]} "
                    f"Include consideration {i} in your explanation."
                ),
                task_type=TaskType.GENERAL,
                complexity=0.8,
            )
        )

    # 20 code-related tasks.
    code_prompts = [
        "def add(a, b): return a + b",
        "class User: pass",
        "import json",
        "function greet() { return 'hello'; }",
        "def square(number): return number * number",
    ]

    for i in range(20):
        tasks.append(
            Task(
                id=f"code-{i:03d}",
                input=f"{code_prompts[i % len(code_prompts)]}\n# Example {i}",
                task_type=TaskType.CODE,
                complexity=0.8,
            )
        )

    # 10 classification tasks.
    for i in range(10):
        tasks.append(
            Task(
                id=f"classification-{i:03d}",
                input=f"Classify the sentiment of this review: example {i}.",
                task_type=TaskType.CLASSIFICATION,
                complexity=0.2,
            )
        )

    # 10 extraction tasks.
    for i in range(10):
        tasks.append(
            Task(
                id=f"extraction-{i:03d}",
                input=f"Extract the key entities from this sample record {i}.",
                task_type=TaskType.EXTRACTION,
                complexity=0.6,
            )
        )

    return tasks
