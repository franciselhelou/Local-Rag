# AI Ritual Local RAG Lab — Student Guide for Windows

## What you will build

This folder contains a small **retrieval-augmented generation (RAG)** application. You will place approved documents in a folder, build an embedding index once, and then ask questions in PowerShell. The application finds the most relevant passages, shows you the retrieved evidence, and asks a language model running **on your own computer** to answer from that evidence.

> **Important boundary:** Software and model downloads require an internet connection during initial setup. After the generator model, embedding model, Python packages, and document index are downloaded or built, questions can run with the network disconnected. Local operation is not a guarantee of “100% security”; use trusted downloads, respect document permissions, and do not use sensitive material without your organisation’s approval.

## Before you begin

You need a Windows 10-or-later computer, internet access for the initial setup, enough free disk space for the models, and permission to use the documents you plan to index. This lab uses English-oriented components and runs most reliably with English documents and questions. The local generator is intentionally small for an 8 GB RAM laptop; answer speed varies across computers.

| Required item | Why it is needed | Where to get it |
| --- | --- | --- |
| Python 3.11 or later | Runs the RAG script and embedding model. | [Python for Windows](https://www.python.org/downloads/windows/) |
| Ollama for Windows | Runs the local language model. | [Ollama Windows download](https://ollama.com/download/windows) |
| This ZIP package | Provides the code, prompt, sample files, notebook, and slides. | Your instructor |
| Internet connection | Required only for initial software and model downloads. | Your normal connection |

## Step 1 — Extract the ZIP package

Download `AI_Ritual_Local_RAG_Student_Package.zip`. In File Explorer, right-click it, choose **Extract All**, and extract it to a location you can find easily, such as your Desktop. Do not run the script while it is still inside the ZIP file.

After extraction, open the new package folder. The important working folder is **`local_rag`**. It contains the files that run the local application.

```text
AI_Ritual_Local_RAG_Student_Package/
│
├── STUDENT_README_FIRST.md
├── AI_Ritual_Two_Hour_Training_Guide.md
├── local_rag/
│   ├── START_HERE_WINDOWS.md          ← you are reading this guide
│   ├── offline_rag.py                 ← the application
│   ├── system_prompt.txt               ← editable assistant policy
│   ├── requirements.txt               ← Python packages to install
│   ├── sample_knowledge_base/          ← first practice documents
│   ├── my_documents/                   ← add your own documents here
│   ├── models/                         ← created automatically after preparation
│   └── rag_index/                      ← created automatically after indexing
├── notebooks/
└── slides/
```

## Step 2 — Install Python

Install Python 3.11 or later from the official Python website. During the installer, select **Add Python to PATH**. When installation is finished, close and reopen PowerShell.

Open PowerShell and confirm that Python is available:

```powershell
py --version
```

You should see a version beginning with `Python 3.11`, `Python 3.12`, or newer. If PowerShell says that `py` is not recognised, restart the computer or reinstall Python with **Add Python to PATH** selected.

## Step 3 — Install Ollama and download the local language model

Install Ollama for Windows from the official download page. Ollama’s Windows download page states that Windows 10 or later is required. [1] After installation, open a new PowerShell window and verify it:

```powershell
ollama --version
```

While connected to the internet, download the small local language model. This is a one-time download of approximately 2 GB.

```powershell
ollama pull llama3.2:3b
```

Confirm that the model is present:

```powershell
ollama list
```

The output should contain `llama3.2:3b`. Do not continue until this command succeeds.

## Step 4 — Open PowerShell in the correct folder

In File Explorer, open the extracted package folder, then open **`local_rag`**. Click the address bar, type `powershell`, and press Enter. A PowerShell window opens in the correct folder.

Alternatively, use `cd` from PowerShell. Replace the example path with the location where you extracted the package:

```powershell
cd "$HOME\Desktop\AI_Ritual_Local_RAG_Student_Package\local_rag"
dir
```

You must see `offline_rag.py`, `system_prompt.txt`, and `requirements.txt` before continuing. If you see only a `.venv` folder and `requirements.txt`, you are one folder too high or have copied only part of the package.

## Step 5 — Create and activate a virtual environment

A virtual environment keeps this workshop’s Python packages separate from the rest of your computer. Run these commands **from inside the `local_rag` folder**:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

When activation succeeds, your command line begins with `(.venv)`. If PowerShell blocks activation, run the following temporary setting and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install --upgrade pip
pip install -r .\requirements.txt
```

Keep the `(.venv)` active whenever you use this local RAG project. If you close PowerShell, repeat Step 4 and then run `\.venv\Scripts\Activate.ps1` again.

## Step 6 — Prepare the embedding model once

Keep the internet connected for this one-time command. It downloads the small embedding model from Hugging Face and saves it inside the local `models` folder.

```powershell
python .\offline_rag.py --prepare
```

Wait for the confirmation that the embedding model is cached. You do **not** need to repeat `--prepare` for every question. Repeat it only if you delete the `models` folder, move the project to a new computer, or the script says that the embedding model is not cached.

## Step 7 — Build the first document index once

An index is a saved collection of document chunks and their embeddings. Building it is the time-consuming step. The program saves the index in `rag_index`, so later questions do **not** need to re-embed every document.

Build an index from the supplied practice documents:

```powershell
python .\offline_rag.py --build-index --offline
```

The script should say that the index was saved and state the number of chunks. Check it at any time with:

```powershell
python .\offline_rag.py --index-status
```

If the index is current, the status says that you can ask questions now.

## Step 8 — Ask your first question

After the index is built, ask a question. You may remain connected to Wi-Fi, but keep `--offline` in the command. It instructs the Hugging Face components to use the cached local model rather than attempting network requests. The language model still runs locally through Ollama.

```powershell
python .\offline_rag.py --offline --question "How should the restaurant respond to an allergy-related concern?"
```

The program first prints **Retrieved evidence**, then prints the **Local answer**. The evidence section matters: inspect whether the retrieved chunks really support the answer and whether the answer cites them as `[S1]`, `[S2]`, and so on.

Ask another question by running the command again. The script now reuses the saved document embeddings, so it should be much faster than the first index build.

```powershell
python .\offline_rag.py --offline --question "What is the cancellation policy for a group of twelve?"
```

## Everyday commands

| What you want to do | Command |
| --- | --- |
| Check that Ollama has the local generator | `ollama list` |
| Download/cache the embedding model for the first time | `python .\offline_rag.py --prepare` |
| Build or replace the index for the default sample folder | `python .\offline_rag.py --build-index --offline` |
| Check whether the index is current | `python .\offline_rag.py --index-status` |
| Ask a question using the default sample folder | `python .\offline_rag.py --offline --question "Your question here"` |
| Use a different number of evidence chunks | Add `--top-k 5` to a question command. |
| Change the assistant behaviour | Edit `system_prompt.txt`, save it, and ask the next question. No index rebuild is needed. |

## Step 9 — Replace the practice documents with your own

Do not alter the supplied `sample_knowledge_base` if you want to keep a known-good test set. Instead, place your own **non-sensitive, permitted** documents in the empty `my_documents` folder.

Open `local_rag\my_documents` in File Explorer and copy in your documents. This version supports the following types:

| Supported type | Use it when | Important note |
| --- | --- | --- |
| `.txt` | You have simple plain text. | Recommended for the most predictable classroom test. |
| `.md` | You have Markdown notes. | Headings and ordinary text are read as text. |
| Text-based `.pdf` | You have a PDF with selectable text. | The script preserves page numbers for source references. |

Microsoft Word `.doc` and `.docx` files are **not supported by this beginner version**. Open a Word document in Word and choose **File → Save As → PDF**, then make sure you can select and copy text from the PDF. A scanned-image PDF must be processed with OCR before this script can retrieve its content reliably.

## Step 10 — Build an index for your own documents

Every document folder has its own index. The saved index remembers which folder it belongs to, so the system will not accidentally answer from an index built for a different folder.

After adding documents to `my_documents`, run:

```powershell
python .\offline_rag.py --build-index --offline --documents .\my_documents
```

Then ask questions from that same folder:

```powershell
python .\offline_rag.py --offline --documents .\my_documents --question "What is the process for approving a refund?"
```

You can check the status of the same document collection:

```powershell
python .\offline_rag.py --index-status --documents .\my_documents
```

> **Rule:** The `--documents` folder used to build the index must be the same folder used when asking questions.

## When to rebuild the index

You must rebuild when a supported document is added, removed, renamed, or edited. The program deliberately stops and displays a rebuild message when it detects a change. This prevents it from silently answering from an old index.

You do **not** rebuild when you only ask a new question. You also do not rebuild after editing `system_prompt.txt`; that file controls the answer policy, not the document evidence.

| Change | Run `--prepare` again? | Run `--build-index` again? |
| --- | --- | --- |
| Ask a different question | No | No |
| Edit `system_prompt.txt` | No | No |
| Add/edit/remove `.txt`, `.md`, or `.pdf` | No | **Yes** |
| Switch from sample documents to `my_documents` | No | **Yes**, for `my_documents` |
| Delete the `rag_index` folder | No | **Yes** |
| Delete the `models` folder or move to another computer | **Yes** | Yes, after preparation |
| Delete the Ollama model | No | No, but run `ollama pull llama3.2:3b` again |

To rebuild your custom document folder after a change:

```powershell
python .\offline_rag.py --build-index --offline --documents .\my_documents
```

## How the system prompt works

The file `system_prompt.txt` is the assistant’s persistent operating policy. The Python script reads it automatically for every question. You do **not** type the system prompt each time.

You may edit this file in Notepad or VS Code to adjust the role, output style, required fields, or escalation wording. Preserve the requirements that the assistant should use retrieved sources, cite source labels, and say when evidence is insufficient unless you have designed and evaluated a different policy.

Example change for an HR policy corpus:

```text
You are a careful internal HR policy assistant.
Answer using only the retrieved policy passages.
Cite every factual claim using [S1], [S2], and so on.
If evidence is insufficient, say that you do not have enough evidence in the supplied documents.
Do not make legal or employment decisions. Recommend escalation to the HR policy owner when needed.
```

## What happens internally

The first `--build-index` command reads the documents, splits them into small overlapping passages, records each passage’s source file and page, and uses the embedding model to convert passages into vectors. It saves those vectors to `rag_index\embeddings.npz` and the source metadata to `rag_index\metadata.json`.

When you ask a question, the program embeds **only your question**, compares it with the saved vectors using cosine similarity, prints the highest-ranked passages, and sends those passages plus your system prompt to the local Ollama model. This is why later questions are faster: the document embeddings are reused.

> RAG does not retrain the language model on your documents. It supplies relevant document passages as working context at question time.

## Troubleshooting

| Symptom | Likely reason | What to do |
| --- | --- | --- |
| `can't open file ... offline_rag.py` | PowerShell is not in the `local_rag` folder. | Use `cd` to enter `local_rag`; run `dir` and confirm that `offline_rag.py` is visible. |
| `ollama` is not recognised | Ollama is not installed or PowerShell needs reopening. | Install Ollama, restart PowerShell, and run `ollama --version`. |
| “model not found” or local generation fails | The local generator is missing. | Run `ollama pull llama3.2:3b`, then `ollama list`. |
| Embedding model is not cached | Step 6 was not completed or `models` was deleted. | Connect to the internet and run `python .\offline_rag.py --prepare`. |
| “No saved embedding index exists” | Documents were never indexed. | Run `python .\offline_rag.py --build-index --offline`. |
| “documents have changed since the index was built” | A source file was added, edited, removed, or renamed. | Rebuild with `--build-index --offline` for the same documents folder. |
| PDF produces no usable chunks | It is likely scanned or image-only. | Use OCR to create a searchable/text-based PDF, then rebuild. |
| Questions remain slow | The local language model is running on a CPU; first model load can also take time. | Close memory-heavy apps, use shorter questions and fewer chunks, or use the Colab notebook for a larger GPU-enabled model. |
| `Activate.ps1` is blocked | PowerShell execution policy is blocking scripts. | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate the environment again. |

## Good practice for students

Start with the supplied sample knowledge base. Ask one question that is clearly answered in the documents, then ask one question the documents cannot answer. Check whether the assistant identifies insufficient evidence rather than inventing a response. Only then introduce a small set of your own approved documents.

Treat a RAG answer as a draft supported by retrieved evidence, not as an unquestionable authority. For important operational, medical, legal, financial, safety, or employment decisions, use a documented human review and escalation process.

## References

[1]: https://ollama.com/download/windows "Ollama — Download for Windows"
[2]: https://huggingface.co/learn/llm-course/en/chapter5/6 "Hugging Face LLM Course — Semantic Search with FAISS"
[3]: https://huggingface.co/docs/hub/en/model-cards "Hugging Face — Model Cards"
[4]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 "Sentence Transformers — all-MiniLM-L6-v2 model card"
