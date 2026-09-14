# Research Notes — Local RAG Workshop

## Sources reviewed

1. Hugging Face, [Use Ollama with any GGUF Model on Hugging Face Hub](https://huggingface.co/docs/hub/en/ollama), accessed 2026-09-06.
   - Ollama is described as an application based on llama.cpp for interacting with LLMs directly on a computer.
   - The documented command format for a Hugging Face GGUF repository is `ollama run hf.co/{username}/{repository}`.
   - Hugging Face states that when available, its Ollama integration defaults to `Q4_K_M`; a named quantization can be selected in the command.
   - The documentation includes `bartowski/Llama-3.2-3B-Instruct-GGUF` as an example repository and demonstrates both low-bit and high-bit quantization tags.

2. Ollama, [Download Ollama on Windows](https://ollama.com/download/windows), accessed 2026-09-06.
   - Ollama provides a Windows installer and a PowerShell installation command.
   - The download page states that Windows 10 or later is required.

## Workshop implication

For a simple Windows-first, air-gapped *after setup* classroom demo, the recommended architecture is a local Ollama runtime running a compact quantized instruct model, combined with local Python retrieval components. The initial installation and model-download steps require internet access; once installers, Python packages, models, and documents are downloaded, the demo can run with the network disconnected. This distinction must be stated explicitly, rather than promising that the first-time installation is offline.

3. Hugging Face, [Semantic Search with FAISS](https://huggingface.co/learn/llm-course/en/chapter5/6), accessed 2026-09-06.
   - The course explains that embeddings can represent sentences, paragraphs, and sometimes documents as vectors.
   - Similarity between a query embedding and document embeddings can be used to return items with the greatest overlap; this supports semantic search beyond literal keyword matching.
   - The course presents FAISS for efficient similarity search at larger scale.

4. Sentence Transformers, [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), accessed 2026-09-06.
   - The model is presented for sentence similarity / feature extraction and has an Apache-2.0 license.
   - The model lineage and naming indicate a MiniLM L6 H384 architecture, supporting 384-dimensional embeddings.

## Architecture decision refined

Use `sentence-transformers/all-MiniLM-L6-v2` for local embeddings, and use NumPy cosine similarity rather than FAISS in the beginner code. This removes a Windows-native dependency from the first session, keeps the retrieval mechanism transparent, and remains adequate for a small teaching corpus. Explain that FAISS or Chroma become attractive when the collection size, filtering, persistence, or retrieval throughput needs exceed the exercise’s scope.

The recommended generative model remains `llama3.2:3b` in a compact quantization supplied by the local runtime. A 3B model is deliberately not marketed as a high-accuracy model; its teaching value lies in fitting constrained hardware and showing grounded answering with sources. The lesson must set a rule: the retrieved passages are evidence, and the model must abstain when they do not support an answer.

5. Hugging Face, [Transformers bitsandbytes quantization](https://huggingface.co/docs/transformers/quantization/bitsandbytes), accessed 2026-09-06.
   - Hugging Face describes bitsandbytes as a quantization library that reduces an LLM’s memory footprint through 8-bit and 4-bit layers.
   - The documented installation command is `pip install --upgrade transformers accelerate bitsandbytes`.
   - The documentation gives the supported `BitsAndBytesConfig` + `from_pretrained(..., device_map="auto")` pattern for quantized loading.
   - The current compatibility table includes NVIDIA T4-or-newer for LLM.int8 and Pascal-or-newer for NF4/FP4; this supports a GPU-enabled Colab design but means the notebook must test for an available GPU and offer a smaller fallback.

## Colab notebook decision

The larger-path notebook will use the free Hugging Face checkpoint `Qwen/Qwen2.5-7B-Instruct` with 4-bit NF4 quantization *only when a CUDA GPU is present*. It will use `transformers`, `accelerate`, and `bitsandbytes`, and it will test `torch.cuda.is_available()` before loading. If a free Colab instance has no compatible GPU, the notebook will provide a clearly marked fallback to a smaller model (e.g., `Qwen/Qwen2.5-1.5B-Instruct`) so the learning activity can still complete rather than failing. The embedding/retrieval layer stays identical to the local version, emphasizing that larger generation capacity does not change RAG’s evidence-retrieval responsibility.

6. Qwen, [Qwen2.5-7B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct), accessed 2026-09-06.
   - The Hub labels this checkpoint for text generation/chat and lists Apache-2.0 as its license.
   - It has an explicit Transformer integration and Colab usage link on the model page, making it an appropriate free-download checkpoint for the larger-model workshop path, subject to Colab GPU availability.

7. Hugging Face, [Model Cards](https://huggingface.co/docs/hub/en/model-cards), accessed 2026-09-06.
   - Hugging Face says a model card should explain the model, intended uses, potential limitations, training and experimental information, datasets used, and evaluation results.
   - The `pipeline_tag` identifies the intended task, reinforcing the practice of selecting a component for its job rather than by a model’s general popularity.

## Final research-backed model selection rubric

Students should start with the business task and operating constraints, then assess the model card rather than starting with a model name. For every component, the rubric checks: task/pipeline tag; input and output language; model capability and known limitations; license and organisational approval; download size, quantization and available RAM/VRAM; runtime and operating-system compatibility; offline operation after preparation; test-set quality; and observability/citations. The deck will distinguish model *parameters* (a rough proxy for capacity) from the resource budget and observed quality on the specific task.

## Branding caution

A public image search returned several unrelated organisations that use “Ritual” in their name. No third-party logo asset will be used without verified provenance. The editable deck will instead use a restrained AI Ritual wordmark treatment and a professional deep-navy/indigo/cyan palette. A client-provided official logo can be substituted later without changing the content.
