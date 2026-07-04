import csv
import json
import os
import time
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file securely
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Paths
INPUT_CSV = r'd:\Web\BISARA AI\bisara-ai-core\datasets\raw\tausug_words_list.csv'
OUTPUT_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\groq_tausug_dataset.jsonl'

# Initialize Groq Client
# Using LLaMA 3 70B - This is a massive, highly intelligent model capable of translating regional languages.
client = Groq(api_key=API_KEY)
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are an expert Tausug linguist and dictionary creator.
You must output ONLY raw JSON. No markdown blocks, no conversational text.
Format strictly as:
{
  "part_of_speech": "Noun/Verb/Adj/etc",
  "english_meaning": "The exact english definition",
  "example_tausug": "A culturally accurate Tausug sentence",
  "example_english": "English translation of the sentence"
}"""

def query_groq(word):
    """Queries the massive LLaMA 3 70B model via Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Define this Tausug word strictly in JSON: {word}"}
            ],
            model=MODEL,
            response_format={"type": "json_object"}, # Forces guaranteed JSON output from Groq
            temperature=0.2, # Low temperature for accurate, factual definitions
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error querying Groq: {e}")
        return None

def main():
    words_to_process = []
    
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            words_to_process.append(row[0])
            
    # Skip the first 100 garbage symbols and process ALL 28,000 words!
    test_words = words_to_process[100:]
    
    print(f"Starting Groq LLaMA-70B generation for {len(test_words)} words...")
    
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    success_count = 0
    
    with open(OUTPUT_JSONL, 'a', encoding='utf-8') as f: # Changed 'w' to 'a' so it appends and doesn't delete if it crashes
        for word in test_words:
            safe_word = word.encode('utf-8', 'replace').decode('utf-8')
            print(f"Asking Groq (Llama-70B) to define: {safe_word}...")
            
            raw_json_str = query_groq(word)
            
            if not raw_json_str:
                print("Failed. Skipping.")
                continue
                
            try:
                ai_data = json.loads(raw_json_str)
                
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
                        "source": "groq_llama70b"
                    }
                }
                
                f.write(json.dumps(conversation) + '\n')
                f.flush()
                print("  -> Success!")
                success_count += 1
                
            except json.JSONDecodeError:
                print(f"  -> Error: Groq returned invalid JSON.")
                
            # Groq free tier has strict rate limits, so we pause 2.5 seconds between words
            time.sleep(2.5)
                
    print(f"\nDone! Generated {success_count} training examples at: {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
