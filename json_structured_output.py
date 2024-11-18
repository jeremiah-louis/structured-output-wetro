import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

json_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "resume_schema",
        "schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the individual",
                },
                "title": {"type": "string", "description": "Title of the individual"},
                "location": {
                    "type": "string",
                    "description": "Current location or address",
                },
                "linkedin": {
                    "type": "string",
                    "description": "LinkedIn profile URL",
                },
                "github": {
                    "type": "string",
                    "description": "GitHub profile URL",
                },
                "contact": {
                    "type": "string",
                    "description": "Phone number or other contact information",
                },
                "email": {"type": "string", "description": "Email address"},
                "summary": {
                    "type": "string",
                    "description": "Brief professional summary or objective statement",
                },
                "years_of_experience": {
                    "type": "integer",
                    "description": "Total years of professional experience",
                },
                "seniority": {
                    "type": "string",
                    "description": "Seniority level of the individual",
                    "enum": ["Junior", "Mid", "Senior", "Lead"],
                },
                "work_experience": {
                    "type": "array",
                    "description": "List of work experiences",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company_name": {
                                "type": "string",
                                "description": "Name of the company",
                            },
                            "position": {
                                "type": "string",
                                "description": "Position or title held at the company",
                            },
                            "duration_years": {
                                "type": "integer",
                                "description": "Duration of employment in years",
                            },
                            "achievements": {
                                "type": "array",
                                "description": "Key achievements in this role",
                                "items": {"type": "string"},
                            },
                        },
                        "required": [
                            "company_name",
                            "position",
                            "duration_years",
                            "achievements",
                        ],
                        "additionalProperties": False,
                    },
                },
                "education": {"type": "string", "description": "Education summary"},
                "skills": {"type": "string", "description": "Skills summary"},
                "certifications": {
                    "type": "string",
                    "description": "Certifications summary",
                },
                "projects": {"type": "string", "description": "Projects summary"},
            },
            "required": [
                "name",
                "title",
                "location",
                "linkedin",
                "github",
                "contact",
                "email",
                "summary",
                "years_of_experience",
                "seniority",
                "work_experience",
                "education",
                "skills",
                "certifications",
                "projects",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


def process_resume() -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "Generate 5 variants of a resume using this schema",
                },
                {"role": "user", "content": ""},
            ],
            response_format=json_schema,
        )
        resume_output = completion.choices[0].message.content
        return resume_output
    except Exception as e:
        print(f"Error processing resume: {e}")


def main():
    resume = process_resume()
    with open("./resume_json_mode.json", "w", encoding="utf-8") as f:
        json.dump(json.loads(resume), f, indent=4, ensure_ascii=False)
    print("Resume has been successfully processed and saved as JSON.")


if __name__ == "__main__":
    main()
