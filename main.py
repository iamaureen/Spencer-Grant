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


def run_prompts_and_save_to_excel(prompt_configs, model, output_file="results.xlsx"):
    """
    Run multiple prompts with different parameters and save results to Excel.
    
    Args:
        prompt_configs: List of dictionaries with keys: quality, identity, ses, genre
        model: The model configuration to use
        output_file: Name of the output Excel file
    """
    results = []
    
    print(f"Running {len(prompt_configs)} prompts...")
    
    for i, config in enumerate(prompt_configs, 1):
        print(f"Processing prompt {i}/{len(prompt_configs)}...")
        
        # Build prompt with parameters
        prompt = build_prompt(
            quality=config.get("quality"),
            identity=config.get("identity"),
            ses=config.get("ses"),
            genre=config.get("genre")
        )
        
        # Execute query
        response_text = execute_single_query(model, prompt)
        
        # Store result with all parameters
        result = {
            "quality": config.get("quality"),
            "identity": config.get("identity"),
            "ses": config.get("ses"),
            "genre": config.get("genre"),
            "response_text": response_text
        }
        
        results.append(result)
        print(f"Completed prompt {i}/{len(prompt_configs)}")
    
    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    print(f"Total prompts processed: {len(results)}")
    
    return results


if __name__ == '__main__':
    base_model = ModelConfig(name="gpt4o", provider="openai",
                             access_token=TEST_LLMs_API_ACCESS_TOKEN,
                             api_url=TEST_LLMs_REST_API_URL
                             )

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
    
    # Run all prompts and save to Excel
    run_prompts_and_save_to_excel(prompt_configs, base_model, output_file="Output/essay_results.xlsx")
    
    print("All prompts completed!")
