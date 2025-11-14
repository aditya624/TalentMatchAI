from langchain_groq import ChatGroq
from langfuse import Langfuse

from tamatai.config import settings
from tamatai.chain.helper import load_prompt, structure_output, format_messages

class Match(object):
    def __init__(self):
        self.langfuse = Langfuse()
        self.prompt = load_prompt(settings, self.langfuse)

        self.model = ChatGroq(
            model=self.prompt["match"]["config"]["model"],
            api_key=settings.groq.api_key
        )

        self.model_with_structure = self.model.with_structured_output(
            structure_output(config=self.prompt["match"]["config"])
        )

    def scoring(self, image_base64):
        messages = format_messages(self.prompt["match"]["prompt"], image_base64)
        output = self.model_with_structure.invoke({"messages": messages})
        output = output.model_dump()
        return output
        