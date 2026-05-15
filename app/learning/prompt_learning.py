from app.learning.memory_store import (
    get_all_edits
)

from app.learning.pattern_extractor import (
    extract_patterns
)


def build_learning_instructions():

    edits = get_all_edits()

    patterns = extract_patterns(edits)

    if not patterns:

        return ""

    instructions = []

    instructions.append(
        "LEARNED IMPROVEMENT PATTERNS:"
    )

    instructions.append(
        (
            "Apply the following drafting "
            "improvements when generating "
            "future legal memos."
        )
    )

    # ----------------------------------------
    # SORT MOST IMPORTANT FIRST
    # ----------------------------------------

    patterns = sorted(
        patterns,
        key=lambda x: x["frequency"],
        reverse=True
    )

    for pattern in patterns:

        pattern_name = pattern["pattern_name"]

        pattern_type = pattern["pattern_type"]

        frequency = pattern["frequency"]

        impact = pattern["impact"]

        instruction = pattern["instruction"]

        examples = pattern["examples"]

        text = f"""
Pattern Name:
{pattern_name}

Pattern Type:
{pattern_type}

Instruction:
{instruction}

Frequency:
{frequency}

Impact:
{impact}
"""

        # ----------------------------------------
        # OPTIONAL EXAMPLE INJECTION
        # ----------------------------------------

        if examples:

            example = examples[0]

            before = example["before"][:200]

            after = example["after"][:200]

            text += f"""

Example Improvement:

Before:
{before}

After:
{after}
"""

        instructions.append(text)

    return "\n".join(instructions)
