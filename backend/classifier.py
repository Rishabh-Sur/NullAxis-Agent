from transformers import pipeline

classifier = pipeline("zero-shot-classification", model=r"backend\models\classifier")
labels = ["Technical Support", "Product Feature Request", "Sales Lead"]
'''
def classify_intent(message: str) -> str:
    message = message.lower()
    if "error" in message or "issue" in message or "problem" in message:
        return "Technical Support"
    elif "feature" in message or "can you add" in message:
        return "Product Feature Request"
    elif "price" in message or "buy" in message or "demo" in message:
        return "Sales Lead"
    return "Unknown"
'''
def classify_intent(query):
    result = classifier(query, labels)
    return result['labels'][0]  # Top prediction
