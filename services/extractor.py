import json

from landingai_ade import LandingAIADE
from utils.schema import build_json_schema


class ExtractorService:

    def __init__(self, api_key: str):
        self.client = LandingAIADE(apikey=api_key)

    @staticmethod
    def build_schema(fields):

        schema = {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }

        for field in fields:

            name = field["name"].strip()

            if not name:
                continue

            schema["properties"][name] = {
                "type": "string",
                "description": field["description"],
            }

            schema["required"].append(name)

        return json.dumps(schema, indent=2)

    def extract(
        self,
        markdown: str,
        fields,
        output_dir,
        instructions: str = "",
        model="extract-latest",
    ):

        enriched_fields = []

        for field in fields:

            description = field["description"]

            if instructions.strip():
                description = (
                    f"{description}\n\n"
                    f"Extraction instructions:\n{instructions}"
                )

            enriched_fields.append(
                {
                    "name": field["name"],
                    "description": description,
                }
            )

        schema = self.build_schema(enriched_fields)

        response = self.client.extract(
            schema=schema,
            markdown=markdown,
            model=model,
            save_to=output_dir,
        )

        return response