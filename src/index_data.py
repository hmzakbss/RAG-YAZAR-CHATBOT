# src/index_data.py
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "all-MiniLM-L6-v2"  # küçük, hızlı ve etkili
EMBED_DIM = 384

def load_txt(path):
    """Metin dosyasını okur ve tek bir string döndürür."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def chunk_text(text, max_len=500):
    """Metni kelime bazlı küçük parçalara ayırır."""
    words = text.split()
    chunks = []
    cur = []
    cur_len = 0
    for w in words:
        cur.append(w)
        cur_len += len(w) + 1
        if cur_len > max_len:
            chunks.append(" ".join(cur))
            cur = []
            cur_len = 0
    if cur:
        chunks.append(" ".join(cur))
    return chunks

def build_index(txt_path, index_path="faiss_index.bin", meta_path="index_meta.pkl"):
    text = load_txt(txt_path)
    chunks = chunk_text(text, max_len=300)

    model = SentenceTransformer(MODEL_NAME)
    print(f"Embedding üretiliyor ({len(chunks)} chunk)...")
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True, batch_size=32)

    # FAISS index
    index = faiss.IndexFlatL2(EMBED_DIM)
    index.add(embeddings.astype(np.float32))
    faiss.write_index(index, index_path)

    with open(meta_path, "wb") as f:
        pickle.dump({"texts": chunks}, f)

    print(f"Index kaydedildi: {index_path}, meta: {meta_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt", required=True, help="Path to TXT dataset")
    parser.add_argument("--index", default="faiss_index.bin")
    parser.add_argument("--meta", default="index_meta.pkl")
    args = parser.parse_args()
    build_index(args.txt, args.index, args.meta)
