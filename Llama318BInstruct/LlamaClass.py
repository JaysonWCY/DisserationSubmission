import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class LlamaModel:
    def __init__(self, model_path):

        self.model_path = os.path.abspath(model_path)

        # Detect device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.device)

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",         
            dtype=torch.float16,
            local_files_only=True
        )

        # Move model to GPU (if available)
        self.model.eval()


    def generate_text(self, prompt):

        # Tokenize the prompt
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        # Move inputs to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=500,
                do_sample=False,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Remove prompt from generated output
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()