"""A transparent local RAG demonstration with a persistent embedding index.

One-time preparation downloads the embedding model from Hugging Face and the generation
model through Ollama. Build the index once after adding or changing documents. Thereafter,
each question only embeds the question, loads the saved vectors, retrieves evidence, and
uses the local Ollama model to answer. No cloud AI API key is required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from ollama import chat
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Downloaded once from Hugging Face, then stored locally in the models directory.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Downloaded once through Ollama, then run locally by Ollama.
GENERATION_MODEL = "llama3.2:3b"
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOCUMENTS = BASE_DIR / "sample_knowledge_base"
CACHE_DIR = BASE_DIR / "models"
SYSTEM_PROMPT_FILE = BASE_DIR / "system_prompt.txt"
INDEX_DIR = BASE_DIR / "rag_index"
INDEX_FILE = INDEX_DIR / "embeddings.npz"
METADATA_FILE = INDEX_DIR / "metadata.json"


@dataclass
class Chunk:
    """A retrievable passage plus the source details shown to the user."""

    source: str
    location: str
    text: str


def supported_files(folder: Path) -> list[Path]:
    """Find the document types intentionally supported in this beginner-friendly lab."""
    extensions = {".txt", ".md", ".pdf"}
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in extensions
        and not path.name.startswith("ADD_YOUR_DOCUMENTS_HERE")
    )


def document_fingerprint(folder: Path) -> str:
    """Create a quick signature from each supported file's path, size, and modified time.

    The signature detects normal additions, removals, and edits. If it changes, the saved
    embeddings are stale and the user must rebuild the index before asking another question.
    """
    files = supported_files(folder)
    if not files:
        raise FileNotFoundError(
            f"No .txt, .md, or text-based .pdf files were found in {folder}. "
            "Add a supported document and run --build-index."
        )
    hasher = hashlib.sha256()
    for path in files:
        stats = path.stat()
        relative = path.relative_to(folder).as_posix()
        hasher.update(f"{relative}|{stats.st_size}|{stats.st_mtime_ns}\n".encode("utf-8"))
    return hasher.hexdigest()


def chunk_text(source: str, location: str, text: str, size: int = 140, overlap: int = 30) -> list[Chunk]:
    """Split text into modest overlapping word chunks, preserving source metadata."""
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    return [
        Chunk(source=source, location=location, text=" ".join(words[start : start + size]))
        for start in range(0, len(words), step)
    ]


def read_documents(folder: Path) -> list[Chunk]:
    """Read .txt, .md, and text-based .pdf files for the index build step."""
    chunks: list[Chunk] = []
    files = supported_files(folder)
    if not files:
        raise FileNotFoundError(
            f"No .txt, .md, or text-based .pdf files were found in {folder}. "
            "Add a supported document and run --build-index."
        )

    for path in files:
        if path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    chunks.extend(chunk_text(path.name, f"page {page_number}", text))
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if text.strip():
                chunks.extend(chunk_text(path.name, "text file", text))

    if not chunks:
        raise ValueError(
            "The supported files contained no extractable text. If your PDF is scanned, "
            "create an OCR/text-based PDF first, then rebuild the index."
        )
    return chunks


def load_embedder(offline: bool) -> SentenceTransformer:
    """Load the embedding model. Offline mode insists on an already-cached copy."""
    if offline:
        # Defence in depth: prevent Hugging Face libraries from requesting missing files.
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    try:
        return SentenceTransformer(
            EMBEDDING_MODEL,
            cache_folder=str(CACHE_DIR),
            local_files_only=offline,
        )
    except OSError as exc:
        if offline:
            raise RuntimeError(
                "The embedding model is not cached locally. Connect once and run "
                "`python offline_rag.py --prepare`, then retry."
            ) from exc
        raise


def build_index(folder: Path, embedder: SentenceTransformer) -> None:
    """Create and save chunk metadata and normalized vectors for reuse across questions."""
    fingerprint = document_fingerprint(folder)
    chunks = read_documents(folder)
    print(f"Building embeddings for {len(chunks)} chunks from {folder} ...")
    embeddings = np.asarray(
        embedder.encode(
            [chunk.text for chunk in chunks],
            normalize_embeddings=True,
            show_progress_bar=True,
        ),
        dtype=np.float32,
    )

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vector_temp = INDEX_DIR / "embeddings.new.npz"
    metadata_temp = INDEX_DIR / "metadata.new.json"
    np.savez_compressed(vector_temp, embeddings=embeddings)
    metadata = {
        "embedding_model": EMBEDDING_MODEL,
        "document_folder": str(folder.resolve()),
        "fingerprint": fingerprint,
        "chunk_count": len(chunks),
        "chunks": [asdict(chunk) for chunk in chunks],
    }
    metadata_temp.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    vector_temp.replace(INDEX_FILE)
    metadata_temp.replace(METADATA_FILE)
    print(f"Index saved in {INDEX_DIR}. Future questions will reuse these {len(chunks)} embeddings.")


def load_index(folder: Path) -> tuple[list[Chunk], np.ndarray]:
    """Load a current index; refuse to answer if documents have changed since indexing."""
    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        raise RuntimeError(
            "No saved embedding index exists. Run `python offline_rag.py --build-index` first."
        )

    metadata = json.loads(METADATA_FILE.read_text(encoding="utf-8"))
    current_folder = str(folder.resolve())
    if metadata.get("embedding_model") != EMBEDDING_MODEL:
        raise RuntimeError("The saved index uses a different embedding model. Run --build-index again.")
    if metadata.get("document_folder") != current_folder:
        raise RuntimeError(
            "The saved index belongs to a different document folder. Run --build-index with this folder."
        )
    if metadata.get("fingerprint") != document_fingerprint(folder):
        raise RuntimeError(
            "Your documents have changed since the index was built. Run `python offline_rag.py "
            "--build-index --offline` before asking questions."
        )

    with np.load(INDEX_FILE, allow_pickle=False) as saved:
        embeddings = np.asarray(saved["embeddings"], dtype=np.float32)
    chunks = [Chunk(**item) for item in metadata["chunks"]]
    if len(chunks) != len(embeddings):
        raise RuntimeError("The saved index is inconsistent. Delete rag_index and run --build-index again.")
    return chunks, embeddings


def show_index_status(folder: Path) -> None:
    """Report whether a usable index exists without loading the embedding model or Ollama."""
    try:
        chunks, _ = load_index(folder)
        print(f"Index status: CURRENT ({len(chunks)} chunks). You can ask questions now.")
    except Exception as exc:
        print(f"Index status: NEEDS BUILD OR REBUILD. {exc}")


def retrieve(question: str, chunks: list[Chunk], corpus_vectors: np.ndarray, embedder: SentenceTransformer, top_k: int) -> list[tuple[Chunk, float]]:
    """Embed only the new question and compare it to the saved normalized vectors."""
    query_vector = np.asarray(embedder.encode(question, normalize_embeddings=True), dtype=np.float32)
    scores = corpus_vectors @ query_vector
    best_indices = np.argsort(scores)[::-1][:top_k]
    return [(chunks[index], float(scores[index])) for index in best_indices]


def answer(question: str, evidence: list[tuple[Chunk, float]]) -> str:
    """Ask the local generator to answer only from the supplied evidence."""
    if not SYSTEM_PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"System prompt file not found: {SYSTEM_PROMPT_FILE}. "
            "Restore system_prompt.txt beside offline_rag.py and retry."
        )
    context_blocks = []
    for source_number, (chunk, score) in enumerate(evidence, start=1):
        context_blocks.append(
            f"[S{source_number}] {chunk.source} ({chunk.location}; relevance={score:.2f})\n{chunk.text}"
        )
    context = "\n\n".join(context_blocks)
    system_prompt = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    user_prompt = f"""Question: {question}

Retrieved sources:
{context}
"""
    response = chat(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0},
    )
    return response.message.content


def prepare() -> None:
    """Perform the one-time Hugging Face embedding-model download and cache it locally."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading/caching {EMBEDDING_MODEL} in {CACHE_DIR} ...")
    load_embedder(offline=False)
    print("Embedding model is cached. Next, ensure `ollama pull llama3.2:3b` has completed.")
    print("Then run `python offline_rag.py --build-index --offline` to index your documents once.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Transparent local RAG demo with a persistent embedding index")
    parser.add_argument("--prepare", action="store_true", help="Download/cache the embedding model once while online.")
    parser.add_argument("--build-index", action="store_true", help="Create or replace the saved embeddings for the document folder.")
    parser.add_argument("--index-status", action="store_true", help="Report whether the saved index matches the documents.")
    parser.add_argument("--documents", type=Path, default=DEFAULT_DOCUMENTS, help="Folder containing .txt, .md, or text-based .pdf files.")
    parser.add_argument("--question", type=str, help="Question to answer from the already-indexed local documents.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of evidence chunks to retrieve; default: 3.")
    parser.add_argument("--offline", action="store_true", help="Use only cached Hugging Face files; no Hub requests.")
    args = parser.parse_args()

    actions = sum([args.prepare, args.build_index, args.index_status])
    if actions > 1:
        parser.error("Use only one of --prepare, --build-index, or --index-status at a time.")

    if args.prepare:
        prepare()
        return
    if args.index_status:
        show_index_status(args.documents)
        return

    if args.build_index:
        embedder = load_embedder(offline=args.offline)
        build_index(args.documents, embedder)
        return

    if not args.question:
        parser.error("Provide --question, or use --prepare, --build-index, or --index-status.")
    if args.top_k < 1:
        parser.error("--top-k must be at least 1.")

    chunks, corpus_vectors = load_index(args.documents)
    embedder = load_embedder(offline=args.offline)
    evidence = retrieve(args.question, chunks, corpus_vectors, embedder, args.top_k)

    print("\nRetrieved evidence")
    print("-" * 72)
    for number, (chunk, score) in enumerate(evidence, start=1):
        print(f"[S{number}] {chunk.source} | {chunk.location} | similarity={score:.3f}")
        print(chunk.text[:300] + ("..." if len(chunk.text) > 300 else ""))
        print()

    print("Local answer")
    print("-" * 72)
    try:
        print(answer(args.question, evidence))
    except Exception as exc:
        raise RuntimeError(
            "The local generation runtime did not answer. Check that Ollama is installed, "
            f"running, and has the `{GENERATION_MODEL}` model. Original error: {exc}"
        ) from exc


if __name__ == "__main__":
    main()
