from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from nasa import search_nasa
import os

app = FastAPI(
    title="NASA Information Retrieval Agent",
    version="1.0"
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "online",
        "agent": "NASA Information Retrieval Agent"
    }


@app.post("/ask")
def ask_agent(request: Question):

    nasa_results = search_nasa(request.question)

    if not nasa_results:
        return {
            "answer": "No relevant NASA results were found.",
            "sources": []
        }

    context = ""

    for result in nasa_results:
        context += f"""
Title: {result.get('title')}
Description: {result.get('description')}
Date: {result.get('date_created')}
NASA ID: {result.get('nasa_id')}
NASA Center: {result.get('center')}
---
"""

    prompt = f"""
You are a NASA information retrieval assistant.

Use ONLY the NASA information provided below.

Do not invent scientific measurements or facts.
If the NASA information does not answer the question,
say that clearly.

Question:
{request.question}

NASA information:
{context}

Give a concise factual answer.
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return {
        "answer": response.output_text,
        "sources": nasa_results
    }
