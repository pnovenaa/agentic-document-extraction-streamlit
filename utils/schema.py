import json


def build_json_schema(fields):
    """
    Build JSON Schema for LandingAI Extract.

    Parameters
    ----------
    fields : list[dict]

    Example
    -------
    [
        {
            "name": "invoice_number",
            "description": "Invoice number"
        }
    ]
    """

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