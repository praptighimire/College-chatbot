from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "microsoft/phi-1_5"

print("⏳ Loading fallback model (Phi 1.5)...")
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    print("✅ Phi-1.5 loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load Phi-1.5: {e}")
    model = None
    tokenizer = None

def fallback_with_phi(user_message: str) -> str:
    if model is None or tokenizer is None:
        return "Sorry, the fallback model is not available right now."
    prompt = f"""You are a helpful assistant for Padma Kanya Multiple Campus.
Please respond kindly and informatively.

User: {user_message}
Assistant:"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
    
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("Assistant:")[-1].strip()