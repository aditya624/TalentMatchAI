from langfuse import Langfuse
from tamatai.config import Settings
from pdf2image import convert_from_bytes
import base64
from pydantic import BaseModel, Field

def structure_output(config):
    description = config["description"]
    class Ranking(BaseModel):
        name: str = Field(..., description=description["name"])
        role: str = Field(..., description=description["role"])
        year_experience: int = Field(..., description=description["year_experience"])
        score: int = Field(..., description=description["score"])
        summary: str = Field(..., description=description["summary"])

    return Ranking
    
def load_prompt(settings: Settings, langfuse: Langfuse):
    system_prompt_loader = langfuse.get_prompt(
        name=settings.langfuse.system_prompt_name,
        version=settings.langfuse.system_prompt_version
    )

    prompt = {
        "match": {
            "langfuse_prompt": system_prompt_loader,
            "prompt": system_prompt_loader.get_langchain_prompt(),
            "config": system_prompt_loader.config
        }
    }

    return prompt

def image_to_base64(image: bytes):
    image_base64 = base64.b64encode(image).decode('utf-8')
    return image_base64

def pdf_to_image_base64(pdf: bytes):
    images = convert_from_bytes(pdf)

    images_base64 = []

    for image in images:
        image_base64 = image_to_base64(image.tobytes())
        images_base64.append(image_base64)

    return images_base64

def format_messages(job_post: str, images_base64: list):

    image_messages = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_base64}",
            },
        } for image_base64 in images_base64
    ]

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract the following job post"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{job_post}",
                    },
                },
                {
                    "type": "text",
                    "text": "Matching with Curiculum Vitae",
                }
            ] + image_messages
        }
    ]

    return messages