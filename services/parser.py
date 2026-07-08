from pathlib import Path

from landingai_ade import LandingAIADE


class ParserService:

    def __init__(self, api_key: str):
        self.client = LandingAIADE(apikey=api_key)

    def parse(
        self,
        document_path: Path,
        output_dir: Path,
        model: str = "dpt-2-latest",
    ):

        response = self.client.parse(
            document=document_path,
            model=model,
            save_to=output_dir,
        )

        markdown = getattr(response, "markdown", "")

        chunks = getattr(response, "chunks", [])

        return {
            "response": response,
            "markdown": markdown,
            "chunks": chunks,
        }