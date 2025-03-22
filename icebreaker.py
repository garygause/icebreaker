import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

def scrape_linkedin_profile(linkedin_profile_url: str, mock_response: bool = False) -> str:
    if mock_response:
        return json.load(open("data/mock_linkedin.json"))
    
    api_endpoint = "https://api.scrapin.io/enrichment/profile"
    params = {
        "linkedInUrl": linkedin_profile_url,
        "apikey": os.getenv("SCRAPIN_API_KEY")
    }
    response = requests.get(api_endpoint, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to scrape LinkedIn profile: {response.status_code} {response.text}")
    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
        and k not in ["peopleAlsoViewed", "certifications"]
    }

    return data
   


if __name__ == "__main__":
    print("LangChain initialized")

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"), temperature=os.getenv("TEMPERATURE")
    )
    summary_template = """
    Given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt = PromptTemplate(
        input_variables="information", template=summary_template
    )

    chain = summary_prompt | llm | StrOutputParser()

    linkedin_data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/garygause/", mock_response=False
    )
    result = chain.invoke(
        {
            "information": linkedin_data
        }
    )
    print(result)
