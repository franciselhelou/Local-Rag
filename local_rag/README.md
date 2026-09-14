# AI Ritual Local RAG Lab

Start with **[START_HERE_WINDOWS.md](START_HERE_WINDOWS.md)**. It is the complete student guide for extracting the package, installing Python and Ollama, creating a virtual environment, adding documents, building/rebuilding the saved index, running questions, editing the system prompt, and solving common Windows errors.

> **Important:** This upgraded version saves document embeddings in `rag_index`. Build the index once after you add or change documents. Later questions reuse that saved index and should be much faster.

## Quick-start sequence

Open PowerShell **inside this `local_rag` folder**. The first three steps need internet access; asking questions does not after preparation.

```powershell
# One time on a new computer
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
ollama pull llama3.2:3b
python .\offline_rag.py --prepare

# One time for the supplied sample documents
python .\offline_rag.py --build-index --offline

# Repeat for each question — it reuses the saved document embeddings
python .\offline_rag.py --offline --question "How should the restaurant respond to an allergy-related concern?"
```

To use your own documents, copy supported `.txt`, `.md`, or text-based `.pdf` files into `my_documents`, then run:

```powershell
python .\offline_rag.py --build-index --offline --documents .\my_documents
python .\offline_rag.py --offline --documents .\my_documents --question "Your question here"
```

Whenever you add, edit, remove, or rename a document, run the relevant `--build-index` command again. You do not need to rebuild when you only change `system_prompt.txt` or ask a new question.
