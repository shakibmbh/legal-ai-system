
from collections import defaultdict
from difflib import ndiff
from datetime import datetime
import re


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def clean_word(word):

    word = word.lower()

    word = re.sub(r"[^\w\s]", "", word)

    return word.strip()


# =========================================================
# PATTERN RULES
# =========================================================

PATTERN_RULES = {

    "stronger_compliance_language": {

        "trigger_words": [
            "must",
            "required",
            "shall",
            "mandatory"
        ],

        "instruction": (
            "Prefer strong compliance wording when "
            "evidence is explicit."
        ),

        "pattern_type": "legal_tone"
    },

    "stronger_legal_certainty": {

        "trigger_words": [
            "states",
            "confirms",
            "establishes",
            "demonstrates"
        ],

        "instruction": (
            "Reduce uncertainty wording when "
            "evidence confidence is high."
        ),

        "pattern_type": "certainty"
    },

    "uncertainty_reduction": {

        "removed_words": [
            "appears",
            "possibly",
            "likely",
            "suggests",
            "may"
        ],

        "instruction": (
            "Avoid uncertain legal language unless "
            "evidence is incomplete."
        ),

        "pattern_type": "certainty"
    },

    "citation_improvement": {

        "trigger_words": [
            "citation",
            "evidence",
            "source",
            "reference"
        ],

        "instruction": (
            "Ensure factual claims include evidence citations."
        ),

        "pattern_type": "grounding"
    },

    "missing_information_section": {

        "trigger_words": [
            "missing",
            "not found",
            "insufficient"
        ],

        "instruction": (
            "Include a missing information section "
            "when evidence gaps exist."
        ),

        "pattern_type": "document_structure"
    }
}


# =========================================================
# DIFF ANALYSIS
# =========================================================

def analyze_diff(original_text, edited_text):

    diff = list(
        ndiff(
            original_text.split(),
            edited_text.split()
        )
    )

    added_words = []
    removed_words = []

    for item in diff:

        if item.startswith("+ "):

            cleaned = clean_word(item[2:])

            if cleaned:

                added_words.append(cleaned)

        elif item.startswith("- "):

            cleaned = clean_word(item[2:])

            if cleaned:

                removed_words.append(cleaned)

    return added_words, removed_words


# =========================================================
# MATCH PATTERNS
# =========================================================

def detect_patterns(
    added_words,
    removed_words,
    original_text,
    edited_text
):

    detected_patterns = []

    # -----------------------------------------
    # RULE-BASED PATTERN MATCHING
    # -----------------------------------------

    for pattern_name, config in PATTERN_RULES.items():

        matched = False

        # Trigger word matching
        for trigger in config.get("trigger_words", []):

            if trigger in added_words:

                matched = True

        # Removed uncertainty matching
        for removed in config.get("removed_words", []):

            if removed in removed_words:

                matched = True

        if matched:

            detected_patterns.append({
                "pattern_name": pattern_name,
                "pattern_type": config["pattern_type"],
                "instruction": config["instruction"]
            })

    # -----------------------------------------
    # STRUCTURAL PATTERNS
    # -----------------------------------------

    original_length = max(
        len(original_text.split()),
        1
    )

    added_ratio = len(added_words) / original_length

    removed_ratio = len(removed_words) / original_length

    if added_ratio > 0.30:

        detected_patterns.append({
            "pattern_name": "expanded_legal_detail",
            "pattern_type": "detail_expansion",
            "instruction": (
                "Provide more detailed legal reasoning "
                "when evidence supports expansion."
            )
        })

    if removed_ratio > 0.20:

        detected_patterns.append({
            "pattern_name": "removed_unnecessary_wording",
            "pattern_type": "conciseness",
            "instruction": (
                "Reduce unnecessary or repetitive wording."
            )
        })

    return detected_patterns


# =========================================================
# IMPACT SCORING
# =========================================================

def calculate_impact(frequency):

    if frequency >= 8:

        return "high"

    elif frequency >= 3:

        return "medium"

    return "low"


# =========================================================
# MAIN PATTERN EXTRACTOR
# =========================================================

def extract_patterns(edits):

    """
    Expected edit structure:

    edit = {
        "draft_id": "...",
        "original_text": "...",
        "edited_text": "...",
        "timestamp": "..."
    }
    """

    pattern_memory = defaultdict(
        lambda: {
            "frequency": 0,
            "examples": [],
            "instruction": "",
            "pattern_type": ""
        }
    )

    for edit in edits:

        original_text = edit[1]
        edited_text = edit[2]

        added_words, removed_words = analyze_diff(
            original_text,
            edited_text
        )

        detected_patterns = detect_patterns(
            added_words,
            removed_words,
            original_text,
            edited_text
        )

        for pattern in detected_patterns:

            name = pattern["pattern_name"]

            pattern_memory[name]["frequency"] += 1

            pattern_memory[name]["instruction"] = (
                pattern["instruction"]
            )

            pattern_memory[name]["pattern_type"] = (
                pattern["pattern_type"]
            )

            # Store examples
            if len(pattern_memory[name]["examples"]) < 5:

                pattern_memory[name]["examples"].append({

                    "before": (
                        original_text[:300]
                    ),

                    "after": (
                        edited_text[:300]
                    )
                })

    # -----------------------------------------
    # FINAL STRUCTURED OUTPUT
    # -----------------------------------------

    learned_patterns = []

    for pattern_name, data in pattern_memory.items():

        learned_patterns.append({

            "pattern_name": pattern_name,

            "pattern_type": data["pattern_type"],

            "frequency": data["frequency"],

            "impact": calculate_impact(
                data["frequency"]
            ),

            "instruction": data["instruction"],

            "examples": data["examples"],

            "last_updated": (
                datetime.utcnow().isoformat()
            )
        })

    return learned_patterns