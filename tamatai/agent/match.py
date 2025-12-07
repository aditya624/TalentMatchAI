from pathlib import Path
from uuid import uuid4

from langchain_groq import ChatGroq
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain.agents import create_agent

from tamatai.config import settings
from tamatai.agent.helper import (
    load_prompt, structure_output, format_messages,
    pdf_to_image_base64,
)
from tamatai.agent.middleware import GroqRetryThenOpenAI

class Match(object):
    def __init__(self):
        self.langfuse = Langfuse()
        self.prompt = load_prompt(settings, self.langfuse)
        self.tmp_dir = Path("./tmp")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent = create_agent(
            model=ChatGroq(
                model=self.prompt["match"]["config"]["model"],
                api_key=settings.groq.api_key
            ),
            system_prompt=self.prompt["match"]["prompt"],
            response_format=structure_output(config=self.prompt["match"]["config"]),
            middleware=[
                GroqRetryThenOpenAI(
                    fallback_model_name=self.prompt["match"]["config"].get("fallback_model", "gpt-5")
                )
            ],
        )

    def scoring(self, job_post_base64: list, file_path: Path):
        image_base64 = pdf_to_image_base64(file_path)
        messages = format_messages(job_post_base64, image_base64)
        output = self.agent.invoke(
            {"messages": messages},config={"callbacks": [CallbackHandler()]}
        )
        result = output["structured_response"]
        return result.model_dump()

    def bulk(self, job_post: bytes, files: list):
        tmp_files: list[Path] = []
        try:
            for file_bytes in files:
                tmp_path = self.tmp_dir / f"{uuid4()}.pdf"
                tmp_path.write_bytes(file_bytes)
                tmp_files.append(tmp_path)

            job_post_path = self.tmp_dir / f"{uuid4()}.pdf"
            job_post_path.write_bytes(job_post)

            job_post_base64 = pdf_to_image_base64(job_post_path)
            scoring_data = [
                self.scoring(job_post_base64, file_path) for file_path in tmp_files
            ]
        finally:
            for file_path in tmp_files:
                try:
                    file_path.unlink()
                except FileNotFoundError:
                    continue

        return scoring_data
