# BISARA AI: The First Open-Source Tausug Language Model

![BISARA AI Banner](https://img.shields.io/badge/Language-Tausug-blue?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-In%20Development-success?style=for-the-badge) ![Creator](https://img.shields.io/badge/Creator-Alnasrif%20Jal--usman%20Haliddin-orange?style=for-the-badge)

## The Story Behind BISARA
For weeks, this project was built on 4 hours of sleep a night. While massive tech companies spent billions of dollars training AI models on English, Mandarin, and Spanish, the Tausug language was completely left behind. 

I refused to let my native tongue be excluded from the AI revolution. 

**BISARA AI** was born out of a relentless dedication to digitize, preserve, and modernize the Tausug language. As a native Tausug speaker and an enthusiast who loves testing and tinkering, I spent countless sleepless nights engineering local data pipelines, gathering over 28,000 Tausug words and phrases from scattered internet archives, and meticulously leveraging my native fluency to manually validate and correct the dataset. 

This repository represents the first step in human history toward building a fully capable, open-source Large Language Model (LLM) specifically trained to understand, speak, and translate Tausug.

---

## Model & Dataset Access

The completed fine-tuned LLaMA-3 adapter model and the curated Tausug dictionary dataset are publicly hosted and available for download on Hugging Face:
*   **Model:** [honeybadgzer/BISARA-Tausug-AI](https://huggingface.co/honeybadgzer/BISARA-Tausug-AI)
*   **Dataset:** [honeybadgzer/tausug-dictionary](https://huggingface.co/datasets/honeybadgzer/tausug-dictionary)

---

## System Architecture & Data Pipeline

To ensure this project remains accessible to students and researchers with limited hardware, the entire data-generation pipeline runs locally using quantized models (Phi-3 / LLaMA 3) via Ollama, requiring zero API costs.

![System Architecture Diagram](images/system_architecture.png)

## QLoRA Training Pipeline

The dataset compiled in this repository is structured in JSONL (ChatML format) to allow for Parameter-Efficient Fine-Tuning (QLoRA) on consumer-grade hardware or free cloud GPUs (like Google Colab).

![QLoRA Training Pipeline Diagram](images/qlora_pipeline.png)

## Repository Structure
*   `datasets/raw/` - Raw manually compiled dictionaries and CSV data.
*   `datasets/processed/` - The final `JSONL` ChatML formatted dataset for Hugging Face.
*   `scripts/` - Automated Python pipelines for data cleaning and local Ollama API communication.
*   `training/` - *(In Development)* QLoRA Hugging Face `SFTTrainer` notebooks.

## Open Source & Community
This project is open-source because language belongs to the people. By releasing this dataset and architecture, I hope to inspire other developers in the Philippines and around the world to build tools that preserve our cultural heritage.

**Created and Architected by:** Alnasrif Jal-usman Haliddin  
**My Cybersecurity & CTF Writeups:** [THE PWNED ARCHIVE](https://nasrif30.github.io/THE-PWNED-ARCHIVE/#archive)  
*For the Tausug People, For the Future.*
