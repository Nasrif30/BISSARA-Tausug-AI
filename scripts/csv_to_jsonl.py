import csv
import json
import os

input_csv = r'd:\Web\BISARA AI\bisara-ai-core\datasets\raw\sample_dictionary.csv'
output_jsonl = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\tausug_instruction_dataset.jsonl'

# Ensure output directory exists
os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)

print("Reading CSV and converting to JSONL Instruction format...")

with open(input_csv, 'r', encoding='utf-8') as csvfile, \
     open(output_jsonl, 'w', encoding='utf-8') as jsonlfile:
    
    reader = csv.DictReader(csvfile)
    count = 0
    
    for row in reader:
        # We construct the ChatML / ShareGPT format needed for AI training
        conversation = {
            "system_prompt": "You are an expert Tausug linguist and AI assistant.",
            "messages": [
                {
                    "role": "user",
                    "content": f"Can you explain the Tausug word '{row['word']}'?"
                },
                {
                    "role": "assistant",
                    "content": f"The word '{row['word']}' is a {row['part_of_speech']} which means '{row['english_meaning']}'.\n\nExample in Tausug: {row['example_tausug']}\nEnglish Translation: {row['example_english']}"
                }
            ],
            "metadata": {
                "source": "manual_sample_test"
            }
        }
        
        # Write exactly one JSON object per line (JSONL format)
        jsonlfile.write(json.dumps(conversation) + '\n')
        count += 1

print(f"Success! Converted {count} dictionary entries into AI training format at: {output_jsonl}")
