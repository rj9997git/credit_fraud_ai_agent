import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def analyze_as_fraud_analyst(question_type, params, results_df):
    llm = get_llm()
    if question_type == "high_value_transactions":
        prompt = f"""
You are a fraud analyst. The user asked to find all transactions over ${params['amount']} in {params['country']}.
Here are the first 5 results:
{results_df.head(5).to_string()}
Total results found: {len(results_df)}
Explain your chain of thought as a fraud analyst.
"""
    elif question_type == "activity_after_inactivity":
        prompt = f"""
You are a fraud analyst. The user asked to find transactions after at least {params['hours']} hours of inactivity,
with an amount at least {params['multiplier']}x the recent average.
Here are the first 5 results:
{results_df.head(5).to_string()}
Total results found: {len(results_df)}
Explain your chain of thought as a fraud analyst.
"""
    elif question_type == "merchant_fraud_rate":
        prompt = f"""
You are a fraud analyst. Here is a summary of merchants and their fraud rates:
{results_df.to_string()}
Explain your chain of thought as a fraud analyst.
"""
    elif question_type == "custom_query":
        prompt = f"""
You are a fraud analyst. The user ran a custom query: "{params['query']}"
Here are the first 5 results:
{results_df.head(5).to_string()}
Total results found: {len(results_df)}
Explain your chain of thought as a fraud analyst.
"""
    result = llm.invoke(prompt)
    return result.content