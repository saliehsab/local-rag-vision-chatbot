# Local RAG Chatbot with Vision (OCR)

<p align="center">
  <img src="https://img.shields.io/badge/AI-RAG%20%2B%20Vision-blue" />
  <img src="https://img.shields.io/badge/Mode-100%25%20Offline-success" />
  <img src="https://img.shields.io/badge/Optimized-Low%20RAM%20(~10GB)-orange" />
  <img src="https://img.shields.io/badge/Backend-Django-green" />
  <img src="https://img.shields.io/badge/LLM-Ollama-black" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

---

## Overview

**Local-RAG-Vision-Chatbot:** A **fully local, privacy-first AI chatbot** powered by **RAG + Vision (OCR)** is a robust integration of Django and Ollama. This project demonstrates how to build an end-to-end Vision-AI application that handles image-to-text extraction, vector indexing with ChromaDB, and context-aware chatting—all fully optimized for consumer-grade hardware.

It enables you to:
- Extract text from complex images with high accuracy.
- Index data into a local vector database for instant retrieval.
- Chat with your documents using an intelligent, privacy-first reasoning engine.

**No cloud. No API. 100% offline.**

---

## Key Highlights

### Fully Offline AI
- Runs entirely on your machine
- No internet required after setup
- Zero data leakage

### Optimized for Low Resources
- Works with **~10GB RAM**
- Uses **quantized models**
- Designed to prevent **OOM crashes**

### Vision + OCR
- Powered by **Qwen2.5-VL:3B**
- Reads:
  - Documents
  - Screenshots
  - Handwritten notes

### Smart RAG System
- Stores extracted data in **ChromaDB**
- Retrieves relevant context for accurate answers

### Conversational AI
- Powered by **Qwen2.5:7B**
- Natural, contextual responses

---

## Tech Stack

- **Backend:** Django 6.x
- **LLM Engine:** Ollama
- **Models:**
  - Qwen2.5:7B (Chat)
  - Qwen2.5-VL:3B (Vision)
- **Vector DB:** ChromaDB
- **Image Processing:** Pillow

---

## Requirements

- Python 3.10+
- Ollama installed
- ~10GB RAM

---

## Installation

```bash
git clone https://github.com/saliehsab/local-rag-vision-chatbot.git
cd chat

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate   # Windows

pip install -r requirements.txt

ollama pull qwen2.5:7b
ollama pull qwen2.5-vl:3b

python manage.py migrate
python manage.py runserver
```

---

## Usage

1. Open: http://127.0.0.1:8000/
2. Upload an image or pdf document
3. Click **Analyze**
4. Ask questions about the content

---

## Optimization Strategy

This project focuses heavily on **efficiency and stability**:

- Quantized LLMs to reduce memory footprint
- Controlled inference pipeline
- Separation of Vision & Chat workloads
- Persistent vector storage

Result:
- No crashes
- Smooth execution on mid-range machines
- Reliable multi-model pipeline

---

## Why This Project?

Most AI systems today:
- Depend on cloud APIs
- Require high-end GPUs

This project proves:
> You can run **RAG + Vision locally**, efficiently, and reliably.

---

## Author

**Elias Hounnou**
  https://www.eliashounnou.dev/
> Building efficient, privacy-first AI systems for real-world constraints.


---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.