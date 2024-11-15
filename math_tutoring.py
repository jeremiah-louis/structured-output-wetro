import json
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str


completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed

# converts the response into a python object
dict_math = math_reasoning.model_dump()

# Stores the json response as a file
with open(file="./math-reasoning.json", mode="w") as f:
    json.dump(dict_math, f)
    print("successful")
