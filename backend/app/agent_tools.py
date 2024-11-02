from openai import OpenAI
import os

def web_search(query: str) -> str:
    '''
    Executes a perplexity search on the web for a given query

    Args:
        query (str): The query to search the web with

    Returns:
        str: The search results
    '''

    pplx_client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

    messages = [
        {"role": "system", "content": "You are a helpful assistant to a financial newsletter writer that can search the web for information. You search for current relevant information about financial topics and companies."},
        {"role": "user", "content": query}
    ]
    print(f"Perplexity is executing query:\n {query}")
    response = pplx_client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
        max_tokens=600,
    )
    print(f"Perplexity response:\n {response.choices[0].message.content}")
    return response.choices[0].message.content