import csv
import json
import requests
import os
import time

# Paths
INPUT_CSV = r'd:\Web\BISARA AI\bisara-ai-core\datasets\raw\tausug_words_list.csv'
OUTPUT_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\ollama_tausug_dataset.jsonl'

# Ollama Settings
# We use llama3 because it is incredibly smart and runs well locally. 
# Make sure you have pulled it: `ollama pull phi3`
OLLAMA_MODEL = "phi3" 
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# The system prompt ensures the model acts strictly as a dictionary engine
SYSTEM_PROMPT = """You are an expert Tausug linguist. 
I will give you a Tausug word. You must return ONLY a raw JSON object with no markdown formatting.
The JSON must have exactly these keys: "part_of_speech", "english_meaning", "example_tausug", "example_english"."""

def query_ollama(word):
    """Queries the local Ollama API to get the definition in JSON format."""
    prompt = f"Tausug word: {word}\nOutput JSON:"
    
    payload = {
        "model": OLLAMA_MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "format": "json" # Forces Ollama to output valid JSON!
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "")
        else:
            print(f"Error from Ollama: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("CRITICAL ERROR: Could not connect to Ollama. Is Ollama running?")
        return None
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def main():
    words_to_process = []
    
    # Read the clean words we exported earlier
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            words_to_process.append(row[0])
            
    # For testing, let's test 10 REAL words by skipping the first 150 garbage symbols
    test_words = words_to_process[150:160]
    print(f"Starting Ollama generation for {len(test_words)} test words...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    
    success_count = 0
    
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
        for word in test_words:
            print(f"Asking Ollama to define: {word}...")
            
            raw_json_str = query_ollama(word)
            
            if not raw_json_str:
                print("Failed. Stopping script.")
                break
                
            try:
                # Parse the AI's string into a Python dictionary
                ai_data = json.loads(raw_json_str)
                
                # Format it into the ChatML / ShareGPT structure for model training
                conversation = {
                    "system_prompt": "You are an expert Tausug linguist and AI assistant.",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Can you explain the Tausug word '{word}'?"
                        },
                        {
                            "role": "assistant",
                            "content": f"The word '{word}' is a {ai_data.get('part_of_speech', 'Word')} which means '{ai_data.get('english_meaning', '')}'.\n\nExample in Tausug: {ai_data.get('example_tausug', '')}\nEnglish Translation: {ai_data.get('example_english', '')}"
                        }
                    ],
                    "metadata": {
                        "source": "ollama_generation"
                    }
                }
                
                # Write to the JSONL dataset
                f.write(json.dumps(conversation) + '\n')
                f.flush() # Force write to disk immediately so we can see it
                print("  -> Success!")
                success_count += 1
                
            except json.JSONDecodeError:
                print(f"  -> Error: Ollama did not return valid JSON. Raw output: {raw_json_str}")
                
    print(f"\nDone! Generated {success_count} training examples at: {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
