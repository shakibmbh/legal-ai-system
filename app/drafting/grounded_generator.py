from google import genai
import json

from app.config import (
    GEMINI_API_KEY,
    CHAT_MODEL
)

from app.learning.prompt_learning import (
    build_learning_instructions
)

# =====================================================
# CLIENT
# =====================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MAX_CHUNKS = 8


# =====================================================
# BUILD EVIDENCE TEXT
# =====================================================

def build_evidence(retrieved_results):

    documents = (
        retrieved_results["documents"][0]
    )[:MAX_CHUNKS]

    ids = (
        retrieved_results["ids"][0]
    )[:MAX_CHUNKS]

    metadatas = (
        retrieved_results["metadatas"][0]
    )[:MAX_CHUNKS]

    evidence_blocks = []

    for doc, chunk_id, meta in zip(
        documents,
        ids,
        metadatas
    ):

        block = f"""
==================================
CHUNK ID: {chunk_id}
PAGE: {meta.get("page", "Unknown")}
SECTION: {meta.get("section", "Unknown")}

TEXT:
{doc}
==================================
"""

        evidence_blocks.append(block)

    return "\n".join(evidence_blocks)


# =====================================================
# BUILD PROMPT
# =====================================================

def build_prompt(
    evidence_text,
    learned_instructions
):

    return f"""
You are an expert legal analyst.

Generate a grounded internal legal memo.

IMPORTANT RULES:

1. ONLY use provided evidence
2. DO NOT hallucinate
3. DO NOT infer missing facts
4. Every factual claim MUST include chunk citations
5. If evidence is missing, explicitly say:
   "Not found in provided evidence."

{learned_instructions}

OUTPUT FORMAT:

Return valid JSON only.

{{
  "key_findings": [],
  "notice_requirements": [],
  "potential_risks": [],
  "missing_information": [],
  "evidence_references": []
}}

EVIDENCE:

{evidence_text}
"""


# =====================================================
# VERIFY OUTPUT
# =====================================================

def verify_output(
    memo_text,
    evidence_text
):

    verification_prompt = f"""
Check whether the memo contains unsupported claims.

If all claims are supported, return:

SUPPORTED

Otherwise return unsupported claims only.

MEMO:
{memo_text}

EVIDENCE:
{evidence_text}
"""

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=verification_prompt
    )

    return response.text


# =====================================================
# MAIN GENERATION FUNCTION
# =====================================================

def generate_memo(retrieved_results):

    # ---------------------------------------------
    # BUILD EVIDENCE
    # ---------------------------------------------

    evidence_text = build_evidence(
        retrieved_results
    )

    # ---------------------------------------------
    # LEARNED PATTERNS
    # ---------------------------------------------

    learned_instructions = (
        build_learning_instructions()
    )

    # ---------------------------------------------
    # BUILD PROMPT
    # ---------------------------------------------

    prompt = build_prompt(
        evidence_text,
        learned_instructions
    )

    # ---------------------------------------------
    # GENERATE
    # ---------------------------------------------

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt
    )

    raw_output = response.text

    # ---------------------------------------------
    # CLEAN JSON
    # ---------------------------------------------

    cleaned_output = (
        raw_output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # ---------------------------------------------
    # PARSE JSON
    # ---------------------------------------------

    try:

        parsed_output = json.loads(
            cleaned_output
        )

    except Exception:

        return {
            "success": False,
            "error": "Invalid JSON response",
            "raw_output": raw_output
        }

    # ---------------------------------------------
    # VERIFY CLAIMS
    # ---------------------------------------------

    verification_result = verify_output(
        raw_output,
        evidence_text
    )

    # ---------------------------------------------
    # RETURN
    # ---------------------------------------------

    return {

        "success": True,

        "memo": parsed_output,

        "verification": verification_result,

        "learning_applied": (
            learned_instructions
        )
    }