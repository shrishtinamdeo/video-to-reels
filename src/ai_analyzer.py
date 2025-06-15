from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_AI_KEY")
)

def get_ai_highlights(segments, total_duration=60):
    example_format = '[{"start": 1.5, "end": 4.2}, {"start": 10.0, "end": 14.3}, ...]'

    # Format the input for GPT
    prompt = f"""
You are an AI that identifies the most engaging moments from a video transcript.
Given the following video transcript with timestamps, select the most interesting segments to make a {total_duration}-second reel.
Return "ONLY" a JSON list of segments with "start" and "end" times that sum up to ~{total_duration} seconds atmost. Nothing else, no extra messages

Return response referring only this example output format: {example_format}

Segments:
"""
    prompt += json.dumps(segments[:30], indent=2)

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",  # or gpt-4 if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        content = response.choices[0].message.content.strip()
        print("This is content---->", content)
        highlights = json.loads(content)
        return highlights
    except Exception as e:
        print(f"❌ Failed to parse AI response: {e}")
        return []