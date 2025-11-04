from config import TEST_LLMs_API_ACCESS_TOKEN, TEST_LLMs_REST_API_URL
from ASUllmAPI import ModelConfig, query_llm
from prompt_builder import build_prompt
import pandas as pd


def execute_single_query(model_name, user_query):
    # Use query_llm module to query ASU GPT.
    # llm_response = query_llm(model=model_name,
    #                          query=user_query)
    llm_response = query_llm(model=model_name,
                             query=user_query,
                             num_retry=3,
                             success_sleep=0.0,
                             fail_sleep=1.0

                             )
    # print(llm_response)
    return llm_response.get('response')


def run_prompts_and_save_to_excel(prompt_configs, models, output_file="results.xlsx"):
    """
    Run multiple prompts with different parameters through multiple models and save results to Excel.
    
    Args:
        prompt_configs: List of dictionaries with keys: quality, identity, ses, genre
        models: List of tuples (model_config, model_name) where model_config is ModelConfig and model_name is string
        output_file: Name of the output Excel file
    """
    results = []
    
    total_combinations = len(prompt_configs) * len(models)
    print(f"Running {len(prompt_configs)} prompts through {len(models)} models ({total_combinations} total combinations)...")
    
    current_count = 0
    
    # Run all prompts for each model before moving to the next model
    for model_config, model_name in models:
        print(f"\n=== Starting all prompts for {model_name} ===")
        
        for config in prompt_configs:
            # Build prompt with parameters
            prompt = build_prompt(
                quality=config.get("quality"),
                identity=config.get("identity"),
                ses=config.get("ses"),
                genre=config.get("genre")
            )
            
            current_count += 1
            print(f"Processing [{current_count}/{total_combinations}] - Model: {model_name}, "
                  f"Quality: {config.get('quality')}, Identity: {config.get('identity')}, "
                  f"SES: {config.get('ses')}, Genre: {config.get('genre')}")
            
            # Execute query
            response_text = execute_single_query(model_config, prompt)
            
            # Store result with all parameters and model name
            result = {
                "model": model_name,
                "quality": config.get("quality"),
                "identity": config.get("identity"),
                "ses": config.get("ses"),
                "genre": config.get("genre"),
                "response_text": response_text
            }
            
            results.append(result)
            print(f"Completed [{current_count}/{total_combinations}]")
        
        print(f"=== Finished all prompts for {model_name} ===\n")
    
    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    print(f"Total combinations processed: {len(results)}")
    
    return results


if __name__ == '__main__':
    # Define multiple models
    models = [
        (ModelConfig(name="gpt4o", provider="openai",
                     access_token=TEST_LLMs_API_ACCESS_TOKEN,
                     api_url=TEST_LLMs_REST_API_URL), "gpt4o"),
        (ModelConfig(name="claude4_sonnet", provider="aws",
                     access_token=TEST_LLMs_API_ACCESS_TOKEN,
                     api_url=TEST_LLMs_REST_API_URL), "claude4_sonnet"),
    ]

    # Define prompt configurations
    prompt_configs = [
        {"quality": "high", "identity": "LatinX", "ses": "low SES", "genre": "educational"},
        {"quality": "high", "identity": "LatinX", "ses": "high SES", "genre": "educational"},
        {"quality": "low", "identity": "LatinX", "ses": "low SES", "genre": "educational"},
        {"quality": "low", "identity": "LatinX", "ses": "high SES", "genre": "educational"},
        {"quality": "high", "identity": "Southern White", "ses": "low SES", "genre": "educational"},
        {"quality": "high", "identity": "Southern White", "ses": "high SES", "genre": "educational"},
        {"quality": "low", "identity": "Southern White", "ses": "low SES", "genre": "educational"},
        {"quality": "low", "identity": "Southern White", "ses": "high SES", "genre": "educational"},
        {"quality": "high", "identity": "LatinX", "ses": "low SES", "genre": "personal"},
        {"quality": "high", "identity": "LatinX", "ses": "high SES", "genre": "personal"},
        {"quality": "low", "identity": "LatinX", "ses": "low SES", "genre": "personal"},
        {"quality": "low", "identity": "LatinX", "ses": "high SES", "genre": "personal"}
    ]
    
    # Run all prompts through all models and save to Excel
    run_prompts_and_save_to_excel(prompt_configs, models, output_file="Output/essay_results_v3.xlsx")
    
    print("All prompts completed!")
