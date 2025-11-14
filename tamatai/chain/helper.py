from langfuse import Langfuse
from tamatai.config import Settings

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

def format_messages(prompt, image_base64):
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract the following image data",
                },
                {
                    "type": "image",
                    "base64": image_base64,
                },
            ]
        }
    ]

    return messages