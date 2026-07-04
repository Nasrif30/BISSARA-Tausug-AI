import csv
import json
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load API key from .env file securely
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Use the modern 2026 Google GenAI Client
client = genai.Client(api_key=API_KEY)

# Paths
INPUT_CSV = r'd:\Web\BISARA AI\bisara-ai-core\datasets\raw\tausug_words_list.csv'
OUTPUT_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\groq_tausug_dataset.jsonl' # We will append to the SAME file!

SYSTEM_PROMPT = """You are an expert Tausug linguist. Define this Tausug word strictly in JSON format matching this schema:
{
  "part_of_speech": "Noun/Verb/Adj/etc",
  "english_meaning": "The exact english definition",
  "example_tausug": "A culturally accurate Tausug sentence",
  "example_english": "English translation of the sentence"
}"""

def query_gemini(word):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{SYSTEM_PROMPT}\n\nWord to define: {word}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        return response.text
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return None

def main():
    words_to_process = []
    
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            words_to_process.append(row[0])
            
    # --- ANTI-DUPLICATION LOGIC ---
    finished_words = set()
    if os.path.exists(OUTPUT_JSONL):
        with open(OUTPUT_JSONL, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    prompt = data["messages"][0]["content"]
                    word = prompt.replace("Can you explain the Tausug word '", "").replace("'?", "")
                    finished_words.add(word)
                except:
                    pass

    # Filter the master list
    test_words = [w for w in words_to_process[100:] if w not in finished_words]
    
    print(f"Starting Modern Google Gemini generation for {len(test_words)} words...")
    
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    success_count = 0
    
    with open(OUTPUT_JSONL, 'a', encoding='utf-8') as f:
        for word in test_words:
            safe_word = word.encode('utf-8', 'replace').decode('utf-8')
            print(f"Asking Gemini to define: {safe_word}...")
            
            raw_json_str = query_gemini(word)
            
            if not raw_json_str:
                print("Failed. Skipping.")
                time.sleep(4.5) 
                continue
                
            try:
                ai_data = json.loads(raw_json_str)
                
                conversation = {
                    "system_prompt": "You are an expert Tausug linguist and AI assistant.",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Can you explain the Tausug word '{safe_word}'?"
                        },
                        {
                            "role": "assistant",
                            "content": f"The word '{safe_word}' is a {ai_data.get('part_of_speech', 'Word')} which means '{ai_data.get('english_meaning', '')}'.\n\nExample in Tausug: {ai_data.get('example_tausug', '')}\nEnglish Translation: {ai_data.get('example_english', '')}"
                        }
                    ],
                    "metadata": {
                        "source": "gemini_flash"
                    }
                }
                
                f.write(json.dumps(conversation) + '\n')
                f.flush()
                print("  -> Success!")
                success_count += 1
                
            except json.JSONDecodeError:
                print(f"  -> Error: Gemini returned invalid JSON.")
                
            time.sleep(4.5)
                
    print(f"\nDone! Generated {success_count} training examples.")

if __name__ == "__main__":
    main()
