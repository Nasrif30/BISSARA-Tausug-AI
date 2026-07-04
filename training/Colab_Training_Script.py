# 1. Install Unsloth & required libraries
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps xformers trl peft accelerate bitsandbytes

import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# 2. Load the Model (We use LLaMA-3 8B, 4-bit quantized for speed)
max_seq_length = 2048 
dtype = None 
load_in_4bit = True 

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# 3. Add LoRA Adapters (This makes training possible on a small GPU)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0, 
    bias = "none",    
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

# 4. Load Your Tausug Dataset from Hugging Face!
dataset = load_dataset("honeybadgzer/tausug-dictionary", split="train")

def formatting_prompts_func(examples):
    prompts = []
    for messages in examples["messages"]:
        # Extract messages
        user_msg = messages[0]["content"]
        assistant_msg = messages[1]["content"]
        
        # Format as ChatML 
        text = f"<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n{assistant_msg}<|im_end|>"
        prompts.append(text)
    return { "text" : prompts }

dataset = dataset.map(formatting_prompts_func, batched = True,)

# 5. Start the Trainer
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        num_train_epochs = 5, # Train for 5 full passes to actually memorize definitions!
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        save_strategy = "no",
    ),
)

print("Starting AI Training...")
trainer_stats = trainer.train()

# 6. Push to Hugging Face
print("Training Complete! Pushing BISARA AI to Hugging Face...")
# Uncomment these lines and add your token when you want to upload the trained model!
# model.push_to_hub("honeybadgzer/BISARA-Tausug-AI", token = "YOUR_HF_TOKEN")
# tokenizer.push_to_hub("honeybadgzer/BISARA-Tausug-AI", token = "YOUR_HF_TOKEN")
