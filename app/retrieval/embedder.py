
import os
import json
import time
import hashlib

from google import genai

from google.genai.errors import ClientError

from app.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)

CACHE_DIR = "./embedding_cache"

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)

def get_cache_path(text):

    text_hash = hashlib.md5(
        text.encode()
    ).hexdigest()

    return f"{CACHE_DIR}/{text_hash}.json"

def get_embedding(text):

    cache_path = get_cache_path(text)

    if os.path.exists(cache_path):

        with open(cache_path, "r") as f:

            cached = json.load(f)

        return cached["embedding"]

    while True:

        try:

            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text
            )

            embedding = (
                response.embeddings[0].values
            )

            with open(cache_path, "w") as f:

                json.dump(
                    {"embedding": embedding},
                    f
                )

            return embedding

        except ClientError as e:

            if "429" in str(e):

                print(
                    "Rate limit hit. Waiting 30 seconds..."
                )

                time.sleep(30)

            else:
                raise e
