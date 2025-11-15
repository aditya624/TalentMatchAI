from langchain_groq import ChatGroq
from langfuse import Langfuse

from tamatai.config import settings
from tamatai.chain.helper import (
    load_prompt, structure_output, format_messages,
    pdf_to_image_base64,
    image_to_base64
)
from langchain.agents import create_agent

class Match(object):
    def __init__(self):
        self.langfuse = Langfuse()
        self.prompt = load_prompt(settings, self.langfuse)
        
        self.agent = create_agent(
            model=ChatGroq(
                model=self.prompt["match"]["config"]["model"],
                api_key=settings.groq.api_key
            ),
            system_prompt=self.prompt["match"]["prompt"],
            tools=[],
            response_format=structure_output(config=self.prompt["match"]["config"])
        )

    def scoring(self, job_post: bytes, file: bytes):
        job_post_base64 = image_to_base64(job_post)
        image_base64 = pdf_to_image_base64(file)
        messages = format_messages(job_post_base64, image_base64)
        output = self.agent.invoke({"messages": messages})
        result = output["structured_response"]
        return result
    
    def bulk(self, job_post: bytes, files: list):
        scoring_data = [
            self.scoring(job_post, file) for file in files
        ]
        return scoring_data
        