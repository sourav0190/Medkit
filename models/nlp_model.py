from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def analyze_notes(text: str):
    """
    Analyze clinical/family notes using BioBERT
    """
    model_name = "dmis-lab/biobert-base-cased-v1.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

    return {"logits": logits.numpy().tolist(), "predicted_class": predicted_class}
