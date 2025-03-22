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
    response = requests.get(
        f"https://api.scrapin.com/linkedin/profile?url={linkedin_profile_url}&apikey={os.getenv('SCRAPIN_API_KEY')}"
    )
    return response.json()


if __name__ == "__main__":
    print("LangChain initialized")

    data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/garygause/", mock_response=True
    )
    print(data)
    exit()

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

    result = chain.invoke(
        {
            "information": "Dr. John Doe is a 32 year old male who is 1.8 meters tall and weighs 80 kilograms. He is a doctor who studied at Harvard University and has a passion for helping people."
        }
    )
    print(result)
