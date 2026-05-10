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
    print('response :: ', llm_response)
    return llm_response.get('response')


def run_prompts_and_save_to_excel(prompt_configs, models, num_runs=1, output_file="results.xlsx"):
    """
    Run multiple prompts with different parameters through multiple models and save results to Excel.
    
    Args:
        prompt_configs: List of dictionaries with keys: quality, identity, ses, genre
        models: List of tuples (model_config, model_name) where model_config is ModelConfig and model_name is string
        num_runs: Number of times to run each prompt configuration (default: 1)
        output_file: Name of the output Excel file
    """
    results = []
    
    total_combinations = len(prompt_configs) * len(models) * num_runs
    print(f"Running {len(prompt_configs)} prompts through {len(models)} models, {num_runs} times each ({total_combinations} total runs)...")
    
    current_count = 0
    
    # Run all prompts for each model before moving to the next model
    for model_config, model_name in models:
        print(f"\n=== Starting all prompts for {model_name} ===")
        
        for config in prompt_configs:
            # Build prompt with parameters (same prompt for all runs)
            prompt = build_prompt(
                quality=config.get("quality"),
                identity=config.get("identity"),
                ses=config.get("ses"),
                genre=config.get("genre")
            )
            
            # Run this prompt num_runs times
            for run_num in range(1, num_runs + 1):
                current_count += 1
                print(f"Processing [{current_count}/{total_combinations}] - Model: {model_name}, "
                      f"Quality: {config.get('quality')}, Identity: {config.get('identity')}, "
                      f"SES: {config.get('ses')}, Genre: {config.get('genre')}, Run: {run_num}/{num_runs}")
                
                # Execute query
                response_text = execute_single_query(model_config, prompt)
                
                # Store result with all parameters, model name, and run number
                result = {
                    "model": model_name,
                    "quality": config.get("quality"),
                    "identity": config.get("identity"),
                    "ses": config.get("ses"),
                    "genre": config.get("genre"),
                    "run_number": run_num,
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
        #RUN MODELS AT A TIME
        # (ModelConfig(name="gpt4o", provider="openai",
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "gpt4o"),
        # (ModelConfig(name="claude4_sonnet", provider="aws",
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "claude4_sonnet"),
        (ModelConfig(name="llama3-405b", provider="aws", #did not have access to llama3_3-70b; #llama3-8b - did not produce some results
                      access_token=TEST_LLMs_API_ACCESS_TOKEN,
                      api_url=TEST_LLMs_REST_API_URL), "llama3")
        # (ModelConfig(name="geminiflash2", provider="gcp-deepmind", #did not have access to geminipro
        #              access_token=TEST_LLMs_API_ACCESS_TOKEN,
        #              api_url=TEST_LLMs_REST_API_URL), "geminiflash2")
        #TODO: add the two other models

    ]

    # Define prompt configurations
    prompt_configs = [
        {"quality": "low", "identity": "LatinX from west coast", "ses": "low SES", "genre": "educational"}, # prompt1
        {"quality": "low", "identity": "LatinX from west coast", "ses": "high SES", "genre": "educational"}, # prompt2
        {"quality": "low", "identity": "African American from south east", "ses": "low SES", "genre": "educational"},  # prompt3
        {"quality": "low", "identity": "African American from south east", "ses": "high SES", "genre": "educational"},  # prompt4
        {"quality": "low", "identity": "Southern White", "ses": "low SES", "genre": "educational"},  # prompt5
        {"quality": "low", "identity": "Southern White", "ses": "high SES", "genre": "educational"},  # prompt6
        {"quality": "low", "identity": "White from midwest", "ses": "low SES", "genre": "educational"},  # prompt7
        {"quality": "low", "identity": "White from midwest", "ses": "high SES", "genre": "educational"},  # prompt8
        {"quality": "low", "identity": "LatinX from west coast", "ses": "low SES", "genre": "personal"},  # prompt9
        {"quality": "low", "identity": "LatinX from west coast", "ses": "high SES", "genre": "personal"},  # prompt10
        {"quality": "low", "identity": "African American from south east", "ses": "low SES", "genre": "personal"},  # prompt11
        {"quality": "low", "identity": "African American from south east", "ses": "high SES", "genre": "personal"},  # prompt12
        {"quality": "low", "identity": "Southern White", "ses": "low SES", "genre": "personal"},  # prompt13
        {"quality": "low", "identity": "Southern White", "ses": "high SES", "genre": "personal"},  # prompt14
        {"quality": "low", "identity": "White from midwest", "ses": "low SES", "genre": "personal"},  # prompt15
        {"quality": "low", "identity": "White from midwest", "ses": "high SES", "genre": "personal"},  # prompt16
        {"quality": "high", "identity": "LatinX from west coast", "ses": "low SES", "genre": "educational"},  # prompt17
        {"quality": "high", "identity": "LatinX from west coast", "ses": "high SES", "genre": "educational"},  # prompt18
        {"quality": "high", "identity": "African American from south east", "ses": "low SES", "genre": "educational"},  # prompt19
        {"quality": "high", "identity": "African American from south east", "ses": "high SES", "genre": "educational"},  # prompt20
        {"quality": "high", "identity": "Southern White", "ses": "low SES", "genre": "educational"},  # prompt21
        {"quality": "high", "identity": "Southern White", "ses": "high SES", "genre": "educational"},  # prompt22
        {"quality": "high", "identity": "White from midwest", "ses": "low SES", "genre": "educational"},  # prompt23
        {"quality": "high", "identity": "White from midwest", "ses": "high SES", "genre": "educational"},  # prompt24
        {"quality": "high", "identity": "LatinX from west coast", "ses": "low SES", "genre": "personal"},  # prompt25
        {"quality": "high", "identity": "LatinX from west coast", "ses": "high SES", "genre": "personal"},  # prompt26
        {"quality": "high", "identity": "African American from south east", "ses": "low SES", "genre": "personal"},  # prompt27
        {"quality": "high", "identity": "African American from south east", "ses": "high SES", "genre": "personal"},  # prompt28
        {"quality": "high", "identity": "Southern White", "ses": "low SES", "genre": "personal"},  # prompt29
        {"quality": "high", "identity": "Southern White", "ses": "high SES", "genre": "personal"},  # prompt30
        {"quality": "high", "identity": "White from midwest", "ses": "low SES", "genre": "personal"},  # prompt31
        {"quality": "high", "identity": "White from midwest", "ses": "high SES", "genre": "personal"}  # prompt32
    ]
    
    # Run all prompts through all models and save to Excel

    run_prompts_and_save_to_excel(prompt_configs, models, num_runs=10, output_file="Output/llama3-405b_essay_results.xlsx")

    
    print("All prompts completed!")
