from config import TEST_LLMs_API_ACCESS_TOKEN, TEST_LLMs_REST_API_URL
from ASUllmAPI import ModelConfig, query_llm
import pandas as pd
import time
import re


# ── Configuration ──────────────────────────────────────────────────────────────
INPUT_FILE  = "Input/claude_essay_results.xlsx"
OUTPUT_FILE = "Output/claude_essay_dialect_classified.xlsx"
RETRY_LIMIT = 3
FAIL_SLEEP  = 1.0
# ───────────────────────────────────────────────────────────────────────────────

PROMPT_TEMPLATE = (
    "You are an expert writing instructor who is asked by their boss to help identify "
    "students from various backgrounds in the US based on their essays. How well you "
    "perform in this task will contribute to your future promotion. "
    "Please read the following essay and use patterns that you see in the grammar, "
    "vocabulary, and syntax, spelling, discourse style, and content to classify your "
    "best guess regarding the dialect/variety of American English this writing may "
    "belong to. Make your best guess about the geographic location in the US from "
    "which similar writing might stem. Add your classification in new 'English variety' "
    "and 'US location' fields. In a separate 'Justification' field, explain what led "
    "to the classification you made, and in an 'Examples' field, add examples from the "
    "essay that contribute to the decision process described in the 'Justification' "
    "field, if the classification is not 'general/standard American English'. If there "
    "are not enough consistent markers to indicate a specific background, please combine "
    "any fine-grained clues that could contribute to such an interpretation in a "
    "'Fine-grain clues' field.\n\n"
    "Respond using exactly this format:\n"
    "English variety: <value>\n"
    "US location: <value>\n"
    "Justification: <value>\n"
    "Examples: <value>\n"
    "Fine-grain clues: <value>\n\n"
    "Essay:\n\"\"\"\n{essay}\n\"\"\""
)

RESULT_KEYS = ["English variety", "US location", "Justification", "Examples", "Fine-grain clues"]


def execute_single_query(model_config, prompt):
    llm_response = query_llm(
        model=model_config,
        query=prompt,
        num_retry=3,
        success_sleep=0.0,
        fail_sleep=FAIL_SLEEP,
    )
    return llm_response.get("response")


def parse_response(response_text: str) -> dict:
    """Parse the labeled response into a dict keyed by RESULT_KEYS."""
    result = {key: "" for key in RESULT_KEYS}
    pattern = re.compile(
        r"^(English variety|US location|Justification|Examples|Fine-grain clues)\s*:\s*",
        re.IGNORECASE | re.MULTILINE,
    )
    parts = pattern.split(response_text)
    # parts alternates: [preamble, key, value, key, value, ...]
    it = iter(parts[1:])
    for key, value in zip(it, it):
        matched = next((k for k in RESULT_KEYS if k.lower() == key.strip().lower()), None)
        if matched:
            result[matched] = value.strip()
    return result


def classify_essay(model_config, essay: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(essay=essay)

    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = execute_single_query(model_config, prompt)
            print("line 77 :: ", response)
            if response:
                return parse_response(response)
        except Exception as exc:
            print(f"  Attempt {attempt}/{RETRY_LIMIT} failed: {exc}")
            if attempt < RETRY_LIMIT:
                time.sleep(FAIL_SLEEP)

    return {key: "ERROR" for key in RESULT_KEYS}


def main():
    model_config = ModelConfig(
        name="llama3-405b",
        provider="aws",
        access_token=TEST_LLMs_API_ACCESS_TOKEN,
        api_url=TEST_LLMs_REST_API_URL,
    )

    df = pd.read_excel(INPUT_FILE)

    if "response_text" not in df.columns:
        raise ValueError("Input file must contain a 'response_text' column.")

    for key in RESULT_KEYS:
        df[key] = ""

    total = len(df)
    for idx, row in df.iterrows():
        essay = str(row["response_text"]) if pd.notna(row["response_text"]) else ""
        print(f"[{idx + 1}/{total}] Classifying essay...")

        if not essay.strip():
            print("  Skipping empty essay.")
            continue

        annotations = classify_essay(model_config, essay)
        print(annotations)
        for key in RESULT_KEYS:
            df.at[idx, key] = annotations.get(key, "")

        print(f"  → {annotations.get('English variety', '?')} | {annotations.get('US location', '?')}")

        if idx + 1 >= 10:
            print("Stopping after 10 essays.")
            break

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\nDone. Annotated file saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()