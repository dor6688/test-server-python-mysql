import openai
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

MEMORY_SYSTEM_PROMPT = """You are a helpful assistant with access to previous conversation history. Use the provided context to give natural, conversational responses that incorporate relevant information from past discussions. Maintain a consistent and friendly tone while seamlessly integrating historical context into your responses. The content has Context from previous conversations 'context' and the specific user quesiton 'query'."""
SIMILARITY_THRESHOLD = 0.8


class OpenAIInterface:
    def __init__(self, api_key: str = os.getenv("OPENAI_KEY")):
        """Initialize the OpenAI interface with API key."""
        openai.api_key = api_key
        self.embedding_model = "text-embedding-3-small"  # "text-embedding-ada-002"
        self.chat_model = "gpt-4o-mini"

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embeddings for a given text using OpenAI's API."""
        try:
            # Generate the embedding for the given text using the OpenAI API
            response = openai.Embedding.create(
                model="text-embedding-ada-002",  # You can use a different model if you prefer
                input=text
            )
            # Extract the embedding from the response
            embedding = response['data'][0]['embedding']
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def generate_response(self, query: str, context: str, ) -> str:
        """Generate a response using relevant conversation pages as context."""

        prompt = f"""Text: {context}

        Question: {query}

        Please answer the question based only on the provided text."""
        response = openai.ChatCompletion.create(
            model=self.chat_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    def is_similar(self, vec1: list[float], vec2: list[float], threshold: float = SIMILARITY_THRESHOLD) -> bool:
        array1, array2 = np.array(vec1), np.array(vec2)
        similarity = np.dot(array1, array2)
        return similarity > threshold

    def generate_summary(self, text):
        """Generate summary for the given text using gpt-3.5-turbo."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for summarization
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Please summarize the following text in 2 lines: {text}"}
                ],
                max_tokens=150,  # Adjust the summary length as needed
                temperature=0.5
            )
            print("aaaaa", response['choices'][0]['message']['content'].strip())
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return None

    def rephrase_text(self, text):
        """Rephrase the given text using gpt-3.5-turbo."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for rephrasing
                messages=[
                    {"role": "system", "content": "You are a rephrasing assistant."},
                    {"role": "user",
                     "content": f"Please rephrase the following sentence for better clarity or grammar in his language: {text}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error rephrasing text: {e}")
            return None
