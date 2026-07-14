from config import TEST_LLMs_API_ACCESS_TOKEN, TEST_LLMs_REST_API_URL
from ASUllmAPI import ModelConfig, query_llm
from prompt_builder import build_prompt
import pandas as pd


def execute_single_query(model_name, user_query):
    llm_response = query_llm(model=model_name,
                             query=user_query,
                             num_retry=3,
                             success_sleep=0.0,
                             fail_sleep=1.0)
    print('response :: ', llm_response)
    return llm_response.get('response')


def run_prompts_and_save_to_excel(prompt_configs, models, num_runs=1, output_file="results.xlsx"):
    """
    Run multiple prompts with different parameters through multiple models and save results to Excel.

    Args:
        prompt_configs: List of dictionaries with keys: quality, identity, ses, text, genre
                        Note: identity and ses are metadata only — not injected into the prompt.
        models: List of tuples (model_config, model_name)
        num_runs: Number of times to run each prompt configuration (default: 1)
        output_file: Name of the output Excel file
    """
    results = []

    total_combinations = len(prompt_configs) * len(models) * num_runs
    print(f"Running {len(prompt_configs)} prompts through {len(models)} models, {num_runs} times each ({total_combinations} total runs)...")

    current_count = 0

    for model_config, model_name in models:
        print(f"\n=== Starting all prompts for {model_name} ===")

        for config in prompt_configs:
            # Build prompt using quality, text, and genre only
            # identity and ses are metadata — not passed to build_prompt
            prompt = build_prompt(
                quality=config.get("quality"),
                text=config.get("text"),
                genre=config.get("genre"),
                implicit_essay=True
            )

            for run_num in range(1, num_runs + 1):
                current_count += 1
                print(f"Processing [{current_count}/{total_combinations}] - Model: {model_name}, "
                      f"Quality: {config.get('quality')}, Identity: {config.get('identity')}, "
                      f"SES: {config.get('ses')}, Genre: {config.get('genre')}, Run: {run_num}/{num_runs}")

                response_text = execute_single_query(model_config, prompt)

                # identity and ses stored as metadata only
                result = {
                    "model": model_name,
                    "quality": config.get("quality"),
                    "identity": config.get("identity"),
                    "ses": config.get("ses"),
                    "genre": config.get("genre"),
                    "text": config.get("text"),
                    "run_number": run_num,
                    "generated_essay": response_text
                }

                results.append(result)
                print(f"Completed [{current_count}/{total_combinations}]")

        print(f"=== Finished all prompts for {model_name} ===\n")

    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    print(f"Total combinations processed: {len(results)}")

    return results


if __name__ == '__main__':

    models = [
        # (ModelConfig(name="gpt4o", provider="openai",
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "gpt4o")
        # (ModelConfig(name="claude4_sonnet", provider="aws",
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "claude4_sonnet")
        # (ModelConfig(name="llama3-405b", provider="aws",
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "llama3")
        (ModelConfig(name="geminiflash3_5", provider="gcp-deepmind",
                     # did not have access to geminipro/geminiflash2 deprecated
                     access_token=TEST_LLMs_API_ACCESS_TOKEN,
                     api_url=TEST_LLMs_REST_API_URL), "geminiflash3_5")
    ]

    # Vignette texts mapped to identity x SES combinations
    VIGNETTES = {
        ("African American from south east", "low SES"): (
            "I grew up in South Memphis, Tennessee, where my family been working long hours just to keep up with rent. "
            "At school, I made the most of what we had, even when our textbooks was outdated, and outside of class I be "
            "spending time at the community center playing basketball with kids from the neighborhood. When I think about "
            "my future, I know ain’t nobody gonna hand it to me, but I’m finna be the first in my family to finish college."
        ),
        ("African American from south east", "high SES"): (
            "I grew up in Cascade Heights, Atlanta, where my family valued education and made sure we had every opportunity "
            "to succeed. At school, I was enrolled in honors courses and had access to tutoring when I needed it, and outside "
            "of class I participated in a leadership program at our church and stayed playing on a travel basketball team. "
            "When I think about my future, I plan to attend a university where I can study business, on God, following in "
            "my parents’ footsteps."
        ),
        ("LatinX from west coast", "low SES"): (
            "I grew up in East Los Angeles, where my family shared a small apartment and my parents would be juggling multiple "
            "jobs, you know. At school, I sometimes struggled to keep up because I was also helping translate — like, at my "
            "parents’ appointments and stuff, and outside of class I helped out at my tío’s taco truck on weekends. When I "
            "think about my future, I want to go to college, even though nobody in my familia has done that before."
        ),
        ("LatinX from west coast", "high SES"): (
            "I grew up in Pasadena, just outside Los Angeles, where mi familia ran a successful catering business that my "
            "grandparents started. At school, I took AP classes and joined the debate team, and outside of class I volunteered "
            "at a local literacy program and played club soccer — you know, staying busy. When I think about my future, I see "
            "myself studying pre-law, something my parents have always encouraged."
        ),
        ("Southern White", "low SES"): (
            "I grew up in a rural town in east Tennessee, where my family got by on my dad’s factory job and whatever my mom "
            "might could pick up seasonally. At school, I did right well, though we didn’t have many advanced classes to choose "
            "from, and outside of class I spent most of my time hunting with my cousins or fixin’ things around the house. "
            "When I think about my future, I reckon a trade certificate might be the most practical path, since a four-year "
            "degree feels out of reach."
        ),
        ("Southern White", "high SES"): (
            "I grew up in a quiet neighborhood in Knoxville, Tennessee, where my family had a comfortable life and my parents "
            "both worked in management. At school, I was in the gifted program and had access to dual enrollment courses at "
            "the community college, and outside of class I was active in 4-H and played varsity baseball. When I think about"
            " my future, I plan to study engineering at a state university, which my parents have been saving for since I was "
            "young — I reckon that makes me pretty fortunate."
        ),
        ("White from midwest", "low SES"): (
            "I grew up in a small farming town in central Iowa, where my family rented a house on the edge of town and money was "
            "always tight. At school, I kept my grades up, though there wasn’t much guidance on how to apply to college — anymore, "
            "it seems like you pretty much need to figure that out yourself, and outside of class I worked shifts at the local "
            "grocery store to help cover my own expenses. When I think about my future, I hope to attend community college, though "
            "I’m still figuring out how to pay for it."
        ),
        ("White from midwest", "high SES"): (
            "I grew up in a suburb outside of Des Moines, Iowa, where my family owned a home and my parents both had steady "
            "careers. At school, I took part in the STEM program and had a college counselor who helped me plan ahead, and "
            "outside of class I played in the school orchestra and volunteered at the county fair every summer. When I think "
            "about my future, I am set on attending a four-year university to study computer science, something my family fully "
            "supports."
        ),
    }

    # Build prompt configs from vignettes
    identities = ["LatinX from west coast", "African American from south east", "Southern White", "White from midwest"]
    ses_levels = ["low SES", "high SES"]
    qualities = ["low", "high"]
    genres = ["educational", "personal"]

    prompt_configs = []
    for quality in qualities:
        for identity in identities:
            for ses in ses_levels:
                for genre in genres:
                    prompt_configs.append({
                        "quality": quality,
                        "identity": identity,
                        "ses": ses,
                        "text": VIGNETTES[(identity, ses)],
                        "genre": genre
                    })

    # 2 quality × 4 identity × 2 SES × 2 genre = 32 configurations
    run_prompts_and_save_to_excel(
        prompt_configs,
        models,
        num_runs=10,
        output_file="Output/exp3_geminiflash3_5_dialect_vignette_essay_results.xlsx"
    )

    print("All prompts completed!")