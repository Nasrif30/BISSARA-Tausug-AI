import json
import os
import re

input_file = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\final_tausug_dataset.jsonl'
output_file = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\final_tausug_dataset_clean.jsonl'
bad_words = ['v', 'n', 'adj', 'adv', 'intj', 'idiom', 'pron', 'rel', 'comp.n', 'comp.adj', 'vag', 'vact', 'vpat', 'vtag', 'vi', 'vt', 'vtpat', 'vipat']

kept = 0
dropped = 0
with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out:
    for line in f:
        data = json.loads(line)
        word = data['messages'][0]['content'].split("'")[1]
        
        # Check for numbers
        has_number = any(char.isdigit() for char in word)
        
        if has_number:
            # Try to strip '2v' or '1n' prefix
            word_clean = re.sub(r'^[0-9]+[a-z]*', '', word)
            if word_clean:
                # Update the word in the messages
                data['messages'][0]['content'] = f"Can you explain the Tausug word '{word_clean}'?"
                data['messages'][1]['content'] = data['messages'][1]['content'].replace(f"The word '{word}'", f"The word '{word_clean}'")
                word = word_clean
                has_number = any(char.isdigit() for char in word)
            
        if word in bad_words or has_number or len(word) < 2:
            dropped += 1
            continue
            
        out.write(json.dumps(data) + '\n')
        kept += 1
        
os.replace(output_file, input_file)
print(f'Cleaned dataset! Kept {kept} words. Dropped {dropped} garbage words.')
