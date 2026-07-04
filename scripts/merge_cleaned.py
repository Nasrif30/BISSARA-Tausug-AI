import json
import os

final_file = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\final_tausug_dataset.jsonl'
cleaned_file = r'd:\Web\BISARA AI\Cleaned_Tausug_Dataset.jsonl'

merged_data = {}

# 1. Load the original final dataset
if os.path.exists(final_file):
    with open(final_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                word = data['messages'][0]['content'].split("'")[1].lower().strip()
                merged_data[word] = data
            except Exception as e:
                pass

original_count = len(merged_data)

# 2. Load the new Cleaned dataset and add/update (fix)
added = 0
if os.path.exists(cleaned_file):
    with open(cleaned_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                word = data['messages'][0]['content'].split("'")[1].lower().strip()
                # 'Fix' by letting the cleaned version take precedence, but 'don't duplicate'
                if word not in merged_data:
                    added += 1
                merged_data[word] = data
            except Exception as e:
                pass

# 3. Save it back to the final file
with open(final_file, 'w', encoding='utf-8') as f:
    for word in sorted(merged_data.keys()):
        f.write(json.dumps(merged_data[word]) + '\n')

print(f'MERGE COMPLETE! Started with {original_count} words. Added {added} new unique words. Total is now {len(merged_data)} words.')
