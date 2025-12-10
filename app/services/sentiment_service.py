import json
import os
from app.services.model import classifier
from app.dto.request import TextInput
from app.util.preprocess_util import preprocess

# Slang dictionary
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "slang_lexicon.json")
with open(file_path, "r", encoding="utf-8") as f:
    slang_dict = json.load(f)

def analyze_sentiment(input: TextInput):
    # Lexicon check
    for word, sentiment in slang_dict.items():
        if word in input.text:
            return {"text": input.text, "sentiment": sentiment, "score": 1.0, "source": "Slang dictionary"}

    # Preprocess
    processed_text = preprocess(input.text)
    result = classifier(processed_text)

    # Set threshold for Neutral status
    threshold = 0.7
    sentiment = result[0]["label"] if result[0]["score"] > threshold else "NEUTRAL"
    
    return {"text": input.text, "sentiment": sentiment, "score": result[0]["score"], "source": "model"}

