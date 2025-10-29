from config import TEST_LLMs_API_ACCESS_TOKEN, TEST_LLMs_REST_API_URL
from ASUllmAPI import ModelConfig, query_llm


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
    print(llm_response)
    return llm_response.get('response')


if __name__ == '__main__':

    base_model = ModelConfig(name="gpt4o", provider="openai",
                             access_token=TEST_LLMs_API_ACCESS_TOKEN,
                             api_url=TEST_LLMs_REST_API_URL
                             )

    query = "What is the capital of phoenix?"


    response_text = execute_single_query(base_model, query)
    print(response_text)

