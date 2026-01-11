from transformers import AutoTokenizer, AutoModelForCausalLM
import torch, os

class LlamaModel:
    def __init__(self, model_path):
        self.model_path = os.path.abspath(model_path)

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",          # Automatically places model layers on available devices
            torch_dtype=torch.float16,  # Use half precision to save memory
            local_files_only=True
        )
        self.model.eval()

    def generate_text(self, prompt, max_new_tokens=80, repetition_penalty=2.0, do_sample=False):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                use_cache=True,
                repetition_penalty=repetition_penalty
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
