from transformers import BertTokenizer, BertModel
import torch
from sentence_transformers import util

class BertProcessor:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()

    def set_model(self, model_name):
        """Switch to a different BERT model."""
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()

    def encode_with_bert(self, text, chunk_size=512, overlap=50):
        """Encode text using BERT with chunking."""
        tokenized_text = self.tokenizer.tokenize(text)
        chunks = [tokenized_text[i:i + chunk_size] for i in range(0, len(tokenized_text), chunk_size - overlap)]
        embeddings = []

        for chunk in chunks:
            input_ids = self.tokenizer.convert_tokens_to_ids(chunk)
            inputs = torch.tensor([input_ids])
            inputs = torch.nn.functional.pad(inputs, (0, chunk_size - len(chunk)), value=self.tokenizer.pad_token_id)
            with torch.no_grad():
                outputs = self.model(inputs)
            embeddings.append(outputs.last_hidden_state[:, 0, :].squeeze())

        final_embeddings = torch.stack(embeddings).mean(dim=0)
        return final_embeddings

    def compare_specs(self, spec1, spec2):
        """Compare two API specs and return similarity."""
        embeddings1 = self.encode_with_bert(spec1)
        embeddings2 = self.encode_with_bert(spec2)
        similarity = util.cos_sim(embeddings1.unsqueeze(0), embeddings2.unsqueeze(0)).item()
        return similarity