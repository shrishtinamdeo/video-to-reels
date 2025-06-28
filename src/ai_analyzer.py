from openai import OpenAI
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_AI_KEY")
)

def get_ai_highlights(segments, total_duration=60):
    example_format = {
        "segments": [
            {"start": 1.5, "end": 4.2},
            {"start": 10.0, "end": 14.3}
        ],
        "caption": "You won't believe what happens next!"
    }

    # Build the prompt
    prompt = f"""
        You are an AI assistant that identifies the most engaging moments from a video transcript.
        Given the following video text segments with timestamps, select the most interesting and meaningful parts to make a {total_duration}-second reel.
        The selected parts should act like a short summary of the entire video.
        Return ONLY a JSON object with two keys:
        - "segments": list of {{ "start": float, "end": float }} objects
        - "caption": short catchy caption (<50 characters)

        The total duration of selected segments should be exactly {total_duration} seconds.

        Example response format:
    """
    prompt += json.dumps(example_format, indent=2)
    prompt += """
    ⚠️ IMPORTANT:
    - Return ONLY the JSON object matching the example.
    - DO NOT add any explanation, markdown, or extra text.
    - Make sure the JSON is valid and parsable.
    """
    prompt += "\n\nSegments:\n"
    prompt += json.dumps(segments[:30], indent=2)
    

    try:
        print("🔍 Prompt sent to AI:\n", prompt)
        
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        print("✅ Raw AI Response:\n", content)

        # Find JSON manually without relying on advanced regex
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1

        if start_idx == -1 or end_idx == -1:
            raise ValueError("❌ No valid JSON found in AI response.")

        json_str = content[start_idx:end_idx]

        # # Fix invalid Unicode escapes (like \u0ba4)
        json_str = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: bytes.fromhex(m.group(1).decode('utf-8')).decode('utf-8', errors='ignore'), json_str.encode().decode('unicode_escape'))
        # json_str = re.sub(r'\\u([0-9a-fA-F]{4})', '', json_str)  # Remove invalid Unicode

        # Fix malformed floats like 14.300000000000001 → 14.3
        json_str = re.sub(r'(\d+\.\d+?)0+(?=\s*[,$])', r'\1', json_str)

        # # Remove control characters
        json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)

        result = json.loads(json_str)

        # for seg in highlights:
        #     if not isinstance(seg, dict) or 'start' not in seg or 'end' not in seg:
        #         print("❌ Invalid segment structure:", seg)
        #         return [], ""

        highlights = result.get("segments", [])
        caption = result.get("caption", "")
        return highlights, caption

    except Exception as e:
        print(f"❌ Failed to parse AI response: {e}")
        return [], ""