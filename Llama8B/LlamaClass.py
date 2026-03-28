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
            device_map=None,          # Disable auto split
            dtype=torch.float16,
            local_files_only=True
        )

        # Move model to GPU (if available)
        self.model.to(self.device)
        self.model.eval()


    def generate_text(self, prompt, max_new_tokens=300):

        # Tokenize plain prompt and move to the correct device
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Remove prompt from generated output
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()