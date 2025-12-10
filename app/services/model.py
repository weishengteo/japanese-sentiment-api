from transformers import pipeline

# Model loading
classifier = pipeline(
    "sentiment-analysis",
    model="koheiduck/bert-japanese-finetuned-sentiment"
)