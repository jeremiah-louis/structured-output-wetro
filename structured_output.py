import os
import json
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import fitz
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SeniorityLevel(str, Enum):
    junior = "Junior"
    mid = "Mid"
    senior = "Senior"
    lead = "Lead"


class WorkExperience(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    position: str = Field(..., description="Position or title held at the company")
    duration_years: int = Field(..., description="Duration of employment in years")
    achievements: List[str] = Field(..., description="Key achievements in this role")


class Resume(BaseModel):
    name: str = Field(..., description="Full name of the individual")
    title: str = Field(..., description="Title of the individual")
    location: str = Field(..., description="Current location or address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    contact: Optional[str] = Field(
        None, description="Phone number or other contact information"
    )
    email: str = Field(..., description="Email address")
    summary: str = Field(
        ..., description="Brief professional summary or objective statement"
    )
    years_of_experience: int = Field(
        ..., description="Total years of professional experience"
    )
    seniority: SeniorityLevel = Field(
        ..., description="Seniority level of the individual"
    )
    work_experience: List[WorkExperience] = Field(
        ..., description="List of work experiences"
    )
    education: str = Field(..., description="Education summary")
    skills: str = Field(..., description="Skills summary")
    certifications: str = Field(..., description="Certifications summary")
    projects: str = Field(..., description="Projects summary")

    def to_json(self, file_path: str):
        """Save the Resume data as a JSON file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, indent=4, ensure_ascii=False)


def read_pdf(file_path: str) -> str:
    pdf_document = fitz.open(file_path)
    all_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        all_text += f"\n{text}"
    return all_text


def process_resume(resume_path: str) -> Resume | None:
    api_key = os.getenv("OPENAI_API_KEY")
    # resume_text = read_pdf(resume_path)
    client = OpenAI(api_key=api_key)
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "What are the requirements needed for a good resume?",
                },
                {"role": "user", "content": ""},
            ],
            response_format=Resume,
        )
        resume_output = completion.choices[0].message.parsed
        return resume_output
    except Exception as e:
        print(f"Error processing resume: {e}")


def main():
    resume = process_resume("./resume.pdf")
    if not resume:
        print("Failed to process the resume.")

    resume.to_json("./resume1.json")
    print("Resume has been successfully processed and saved as JSON.")


if __name__ == "__main__":
    main()
