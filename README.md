# BISSARA AI: The First Open-Source Tausug Language Model

![BISSARA AI Banner](https://img.shields.io/badge/Language-Tausug-blue?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-In%20Development-success?style=for-the-badge) ![Creator](https://img.shields.io/badge/Creator-Alnasrif%20Jal--usman%20Haliddin-orange?style=for-the-badge)

## The Story Behind BISSARA AI

For weeks, this project was built on just four hours of sleep each night. While major technology companies invested billions into AI for widely spoken languages such as English, Mandarin, and Spanish, the Tausug language remained largely absent from modern language models.

I refused to let my native language be left behind.

**BISSARA AI** was created to help preserve, digitize, and modernize the Tausug language through open-source artificial intelligence. As a native Tausug speaker, I spent countless hours collecting, validating, correcting, and organizing linguistic data from dictionaries, educational resources, and publicly available references while manually reviewing every entry using my own fluency.

This repository represents an important milestone toward building a fully capable open-source Large Language Model (LLM) designed to understand, generate, and translate the Tausug language.

---

# History

BISSARA AI is presented as **the first open-source Tausug language AI model**, created and architected by **Alnasrif Jal-usman Haliddin**, with the goal of making Tausug language technology freely accessible for researchers, developers, students, and the Tausug community.

---


## Model & Dataset Access

The completed fine-tuned LLaMA-3 adapter model and the curated Tausug dataset are publicly available on Hugging Face.

**Model**
- https://huggingface.co/honeybadgzer/BISSARA-Tausug-v1.0-Beta-GGUF

**Dataset**
- https://huggingface.co/datasets/honeybadgzer/tausug-dictionary

---

## System Architecture & Data Pipeline

To ensure accessibility for students and researchers with limited hardware, the entire data-generation pipeline runs locally using quantized models through Ollama, requiring no paid API services.

<img width="2845" height="6772" alt="Data Pipeline Diagram-2026-07-04-211613" src="https://github.com/user-attachments/assets/17ff6610-5f4f-4ca6-bcb2-33dcd8590f11" />

---

## QLoRA Training Pipeline

The dataset is formatted in ChatML (JSONL) for efficient parameter-efficient fine-tuning (QLoRA), allowing training on consumer hardware and free cloud GPU platforms.

<img width="8192" height="794" alt="Deep Learning_Training Diagram-2026-07-04-211707" src="https://github.com/user-attachments/assets/4d706115-577b-43b8-843d-f7fc49ae98d6" />

---

## Repository Structure

- `datasets/raw/` — Raw dictionaries and collected linguistic resources.
- `datasets/processed/` — Final ChatML (JSONL) datasets.
- `scripts/` — Data-cleaning and Ollama automation pipelines.
- `training/` — QLoRA training notebooks and experiments.

---

## Additional Documentation

For licensing, citations, and technical documentation, see the following files:
---

## Copyright & License

Copyright © 2026 **Alnasrif Jal-usman Haliddin**.

BISSARA AI is released under the **Apache License 2.0**.

### Additional Project Documentation

- **LICENSE** – Apache License 2.0  
  https://github.com/Nasrif30/BISSARA-Tausug-AI/blob/main/LICENSE

- **CITATION.cff** – Citation metadata for GitHub's **"Cite this repository"** feature  
  https://github.com/Nasrif30/BISSARA-Tausug-AI/blob/main/CITATION.cff

- **README_Phase2_v1.md** – Complete documentation for BISSARA AI Phase 2 Version 1  
  https://github.com/Nasrif30/BISSARA-Tausug-AI/blob/main/README_Phase2_v1.md

See the **LICENSE** file for the complete license terms.


---

## Open Source & Community

BISSARA AI is open source because language belongs to its people.

The project aims to encourage students, researchers, educators, and developers to build technologies that help preserve and advance the Tausug language for future generations.

---

## Copyright & License

Copyright © 2026 **Alnasrif Jal-usman Haliddin**. All rights reserved.

BISSARA AI is an open-source project released under the **Apache License 2.0**.

You are welcome to use, study, modify, and redistribute this project in accordance with the terms of the license. If you build upon BISSARA AI, its datasets, documentation, or architecture, attribution to the original creator is appreciated and helps support the continued development of open-source AI for underrepresented languages.

See the [LICENSE](LICENSE) file for the complete license text.

---

## Creator

**Created & Architected by**

**Alnasrif Jal-usman Haliddin**

GitHub  
https://github.com/Nasrif30

Hugging Face  
https://huggingface.co/honeybadgzer

Cybersecurity Portfolio  
https://nasrif30.github.io/THE-PWNED-ARCHIVE/#archive

---

*"For the Tausug People. For the Future."*
