import os
from datasets import load_dataset
from huggingface_hub import login, HfApi
from dotenv import load_dotenv

def main():
    print("Loading Hugging Face Token...")
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token:
        print("Error: HF_TOKEN not found in .env file!")
        return

    # Log in to Hugging Face
    login(token=hf_token)
    
    # Path to the final dataset
    dataset_path = r'd:\Web\BISARA AI\bisara-ai-core\datasets\processed\final_tausug_dataset.jsonl'
    
    print(f"Loading local dataset from: {dataset_path}")
    
    try:
        # Load the JSONL file as a Hugging Face Dataset
        dataset = load_dataset("json", data_files=dataset_path, split="train")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    # Automatically get your Hugging Face username
    api = HfApi()
    user_info = api.whoami(token=hf_token)
    username = user_info['name']
    
    repo_id = f"{username}/tausug-dictionary"
    
    print(f"\nUploading dataset to Hugging Face Hub at: {repo_id}...")
    print("Please wait, this might take a few seconds...")
    
    # Push to hub
    dataset.push_to_hub(repo_id, private=False)
    
    print("\nSUCCESS! Dataset pushed successfully! 🎉")
    print(f"You can now view your dataset worldwide here: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    main()
