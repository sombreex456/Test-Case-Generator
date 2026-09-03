import os
import json

from dotenv import load_dotenv
from anthropic import Anthropic

from models import TestCase


load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def generate_test_cases(requirement: str) -> list[TestCase]:

    prompt = f"""
You are an experienced software tester.

Generate between 8 and 12 high-quality test cases specifically for this software requirement:

{requirement}

Include a suitable mixture of:
- Positive test cases
- Negative test cases
- Boundary or edge cases where relevant
- Security test cases where relevant

For every test case provide:
- id
- title
- test_type
- priority
- preconditions
- steps
- expected_result

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include ```json.
- Do NOT include explanations before or after the JSON.
- Make sure every string is enclosed in double quotes.
- Make sure every item in an array is separated by a comma.
- Make sure the JSON starts with [ and ends with ].
- Do not generate duplicate test cases.

Use exactly this structure:

[
    {{
        "id": "TC001",
        "title": "Example title",
        "test_type": "Positive",
        "priority": "High",
        "preconditions": "Example precondition",
        "steps": [
            "Step 1",
            "Step 2"
        ],
        "expected_result": "Example expected result"
    }}
]
"""

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_text = next(
        block.text
        for block in response.content
        if block.type == "text"
    )

    # Remove accidental markdown code fences if Claude adds them
    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        test_cases_data = json.loads(response_text)

    except json.JSONDecodeError as e:

        print("Claude returned invalid JSON.")
        print("Error:", e)
        print("Response from Claude:")
        print(response_text)

        raise ValueError(
            "Claude returned an invalid JSON response. "
            "Please try generating the test cases again."
        )

    test_cases = [
        TestCase(**test_case)
        for test_case in test_cases_data
    ]

    return test_cases