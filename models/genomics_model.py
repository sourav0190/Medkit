from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

def get_dna_embedding(sequence: str):
    """
    Generate DNA embeddings using Nucleotide Transformer v2
    """
    model_name = "InstaDeepAI/nucleotide-transformer-v2-500m-multi-species"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForMaskedLM.from_pretrained(model_name, trust_remote_code=True)

    # Tokenize sequence
    inputs = tokenizer(sequence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    # Take last hidden state as embedding
    embedding = outputs.hidden_states[-1].mean(dim=1)
    return embedding.numpy()
