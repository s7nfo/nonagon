import json

from openai import OpenAI


class Extractor:
    def __init__(self, api_key: str) -> None:
        """
        "Extractor is a class for extracting and deduplicating feature requests and bug reports from text."

        Args:
            api_key (str): API key for accessing the OpenAI services.
        """

        self.client = OpenAI(api_key=api_key)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "submit_feature_request",
                    "description": "Submits a feature request",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Succinct description of the feature request",
                            },
                            "related_tickets": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of IDs for tickets containing similar feature requests",
                            },
                        },
                        "required": ["description", "related_tickets"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "submit_bug_report",
                    "description": "Submits a bug report",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Succinct description of the bug",
                            },
                            "related_tickets": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of IDs for tickets containing similar bug reports",
                            },
                        },
                        "required": ["description", "related_tickets"],
                    },
                },
            },
        ]

    def extract(self, text: str, existing_tickets: list[(str, str)]) -> dict[str, str]:
        """
        Extract feature requests and bug reports from text and deduplicate against existing tickets.
        Assumes there's at most one feature request and one bug report in the text.

        Args:
            text (str): Text to be analyzed.
            existing_tickets (list of tuple of str (ticket id), str (ticket title)): Information about
            existing tickets to be used for deduplication.

        Returns:
            dict of str, str: A dictionary with 'feature_request' and 'bug_report' as keys
            and the first relevant, non-duplicate parsed argument or None as values.
        """

        messages = [
            {
                "role": "system",
                "content": f"""Analyse the following text and report a summary of each feature request or bug report using the submit_feature_request and submit_bug_report functions.
                    A feature request is when someone asks for a new feature or improvement. A bug report is when someone reports a bug or problem.
                    The summary should be concise and make it easy for engineers and product managers to understand the request or report.
                    If the feature request or bug report matches any existing tickets, please also list their IDs.

                    Existing tickets: {existing_tickets}
                """,
            },
            {"role": "user", "content": text},
        ]

        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            tools=self.tools,
            seed=42,
            temperature=0.0,
        )

        response_message = response.choices[0].message
        result = {"feature_request": None, "bug_report": None}

        if response_message.tool_calls:
            result["feature_request"] = next(
                (
                    json.loads(c.function.arguments)
                    for c in response_message.tool_calls
                    if c.function.name == "submit_feature_request"
                ),
                None,
            )
            result["bug_report"] = next(
                (
                    json.loads(c.function.arguments)
                    for c in response_message.tool_calls
                    if c.function.name == "submit_bug_report"
                ),
                None,
            )

        return result
