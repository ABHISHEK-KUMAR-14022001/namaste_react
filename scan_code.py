import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Replace with your Hugging Face API key
HUGGINGFACE_API_KEY = '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'
MODEL_NAME = 'openbmb/MiniCPM-o-2_6'

def scan_code_for_bugs(code_snippet):
    headers = {
        'Authorization': f'Bearer {HUGGINGFACE_API_KEY}'
    }
    
    # Initialize model and tokenizer from Hugging Face
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # Tokenize the JavaScript code snippet
    inputs = tokenizer(code_snippet, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    # Get predictions
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax().item()
    
    return predicted_class  # You can map predicted_class to bug/error categories if needed

if __name__ == '__main__':
    # Example JavaScript code snippet from repo
    code_snippet = """
    function buggyFunction() {
        var a = 1;
        var b = "string";
        return a + b;  // This will cause a type error
    }
    """
    
    # Call the function to scan the code
    result = scan_code_for_bugs(code_snippet)
    print("Scan result:", result)
