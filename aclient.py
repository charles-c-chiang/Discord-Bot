import openai
from openai import AsyncAzureOpenAI
import os
import json
import asyncio

# get API key from auth.json
f = open('auth.json')
OPENAI_API_KEY = json.load(f)['OPENAI_API_KEY']

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')

client = AsyncAzureOpenAI(api_key = OPENAI_API_KEY,
    api_version = "2023-07-01-preview", 
    azure_endpoint="https://charlietest.openai.azure.com/openai/deployments/charlieTestModel/chat/completions?api-version=2023-07-01-preview")

async def main() -> None:
        
    completion = await client.chat.completions.create(
        model="deployment-name",  # e.g. gpt-35-instant
        messages=[
            {
                "role": "system",
                "content": "You are StrangerBot, an introduction chatbot. Your job is to interact with two different strangers, and help them get to know each other better. You can do this by recommending them topics to talk about or asking them to share more about themselves. You should start each conversation by introducing yourself, then by asking both people their name and some basic facts about them. You should not have overly lengthy or detailed responses, as the focus of the conversation should be between the two strangers and you want to keep a friendly, casual tone.",
            },
            {
                "role": "user",
                "content": "Hello, my name is Charlie"
            },
        ],
    )
    # print(completion.model_dump_json(indent=2))
    print(completion.choices[0].message.content)

asyncio.run(main())

#import openai
# Possibly outdated
# openai.api_type = "azure"
# openai.api_base = "https://charlietest.openai.azure.com/"
# openai.api_version = "2023-07-01-preview"
# openai.api_key = os.getenv(OPENAI_API_KEY)

# message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]

# completion = openai.ChatCompletion.create(
#   engine="charlieTestModel",
#   messages = message_text,
#   temperature=0.7,
#   max_tokens=800,
#   top_p=0.95,
#   frequency_penalty=0,
#   presence_penalty=0,
#   stop=None
# )

# print(completion.choices[0].text)
