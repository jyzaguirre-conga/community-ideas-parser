import anthropic
import json
from config import ANTHROPIC_API_KEY

class ClaudeAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def analyze_ideas(self, json_data, max_retries=3):
        prompt = f"""
        Please analyze the following JSON data containing ideas scraped from the Conga community website. For each idea, the data includes the title, author, content, number of votes, and comments.

        Your task is to generate a concise summary and analysis of the ideas based on the provided data. The summary should include:

        1. A brief overview of the main themes or topics covered by the ideas.
        2. Identification of the top 3 ideas with the most votes, along with their titles and vote counts.
        3. A sentiment analysis of the comments, indicating whether the overall sentiment is positive, negative, or neutral.
        4. Any notable patterns, trends, or insights you can derive from the data.

        Please format your response as a JSON object with the following structure:
        {{
            "sections": [
                {{
                    "title": "Section Title",
                    "content": "Section content in Markdown format"
                }},
                ...
            ],
            "table": "| Sentiment Score | Toxicity Score |\\n|-----------------|----------------|\\n| sentiment_score | toxicity_score |"
        }}

        Replace "sentiment_score" and "toxicity_score" with the actual values in the table.
        - Sentiment Score: 1-5, where 1 is very negative and 5 is very positive
        - Toxicity Score: 1-5, where 1 is non-toxic and 5 is very toxic and profane

        Here is the JSON data:

        {json_data}
        """

        retry_count = 0
        while retry_count < max_retries:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=3072,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            print(f"Response content: {response.content}")

            # Find the first TextBlock in the response content
            for block in response.content:
                print(f"Block type: {block.type}")
                if block.type == "text":
                    print(f"TextBlock content: {block.text}")
                    json_start = block.text.find("{")
                    json_end = block.text.rfind("}")
                    if json_start != -1 and json_end != -1:
                        json_content = block.text[json_start:json_end+1]
                        try:
                            json_data = json.loads(json_content)
                            if "sections" in json_data and "table" in json_data:
                                return json_data
                            else:
                                print("JSON response is missing required fields. Retrying...")
                                retry_count += 1
                                break
                        except json.JSONDecodeError:
                            print("Invalid JSON format in the response. Retrying...")
                            retry_count += 1
                            break

        print("Failed to receive a valid JSON response after maximum retries.")
        return None

