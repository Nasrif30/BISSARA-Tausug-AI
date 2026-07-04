import json
import os

# Paths
WEBONARY_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\webonary_parsed_dataset.jsonl'
GROQ_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\groq_tausug_dataset.jsonl'
FINAL_JSONL = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\final_tausug_dataset.jsonl'

def extract_word_from_prompt(prompt):
    # The prompt format is: "Can you explain the Tausug word '{word}'?"
    try:
        word = prompt.split("'")[1]
        return word.lower().strip()
    except:
        return None

def main():
    merged_data = {}
    
    # 1. Load Webonary Data First (HIGHEST PRIORITY)
    webonary_count = 0
    if os.path.exists(WEBONARY_JSONL):
        print("Loading high-quality Webonary data...")
        with open(WEBONARY_JSONL, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    prompt = data["messages"][0]["content"]
                    word = extract_word_from_prompt(prompt)
                    if word:
                        merged_data[word] = data
                        webonary_count += 1
                except:
                    pass
        print(f"Loaded {webonary_count} human-verified words.")
    else:
        print("Webonary dataset not found yet (Make sure to run parse_webonary_text.py first).")

    # 2. Load Groq Data (LOWER PRIORITY - DO NOT OVERWRITE)
    groq_count = 0
    skipped_count = 0
    if os.path.exists(GROQ_JSONL):
        print("\nLoading Groq AI generated data...")
        with open(GROQ_JSONL, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    prompt = data["messages"][0]["content"]
                    word = extract_word_from_prompt(prompt)
                    if word:
                        # Only add if the word doesn't already exist from Webonary
                        if word not in merged_data:
                            merged_data[word] = data
                            groq_count += 1
                        else:
                            skipped_count += 1
                except:
                    pass
        print(f"Loaded {groq_count} AI words.")
        print(f"Skipped {skipped_count} AI words because Webonary already defined them better!")
    
    # 3. Save the final dataset
    os.makedirs(os.path.dirname(FINAL_JSONL), exist_ok=True)
    print(f"\nSaving {len(merged_data)} unique words to {FINAL_JSONL}...")
    
    with open(FINAL_JSONL, 'w', encoding='utf-8') as f:
        for word in sorted(merged_data.keys()):
            f.write(json.dumps(merged_data[word]) + '\n')
            
    print("Done! The final duplicate-free dataset is ready for Hugging Face!")

if __name__ == "__main__":
    main()
