# Start Here — AI Ritual Local RAG Student Package

Welcome. This package contains a Windows-first local RAG exercise, a detailed setup guide, a Google Colab comparison notebook, and the workshop presentation. You need to follow only one document first:

> Open **`local_rag\START_HERE_WINDOWS.md`** and complete its steps in order.

## Package map

| Folder or file | What it contains | When to use it |
| --- | --- | --- |
| `local_rag\START_HERE_WINDOWS.md` | Complete Windows installation, setup, indexing, document-update, and troubleshooting guide. | **Start here.** |
| `local_rag\offline_rag.py` | The local RAG application. | Run it through PowerShell following the student guide. |
| `local_rag\system_prompt.txt` | The editable policy for the local assistant. | Edit when you want to change assistant behaviour; no re-index is needed. |
| `local_rag\sample_knowledge_base` | Fictional restaurant documents for safe first experiments. | Use for the first index and questions. |
| `local_rag\my_documents` | Empty folder for your own permitted documents. | Add `.txt`, `.md`, or text-based `.pdf` files here. |
| `notebooks\ai_ritual_colab_rag.ipynb` | GPU-enabled Google Colab version using a larger model. | Use only after the local exercise; do not upload confidential data. |
| `slides` | Editable workshop presentation and source files. | Use for teaching or review. |
| `AI_Ritual_Two_Hour_Training_Guide.md` | Detailed instructor agenda and AI opportunity-selection framework. | Use if facilitating the two-hour session. |

## The command pattern to remember

The local RAG now uses **a saved embedding index**. Build the index after document changes, then ask as many questions as you like.

```powershell
# Build once after adding/changing documents
python .\offline_rag.py --build-index --offline --documents .\my_documents

# Ask many questions using the already-saved index
python .\offline_rag.py --offline --documents .\my_documents --question "Your question here"
```

Do not put confidential, personal, regulated, or client-owned documents into the Colab notebook without explicit organisational approval. For the local lab, “offline” becomes possible after the initial software and model downloads and after the index has been built.
