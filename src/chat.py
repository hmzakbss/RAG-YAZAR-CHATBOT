import streamlit as st
import os
import pickle
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# -------------------------
# .env ve API Key
# -------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------
# Ayarlar
# -------------------------
DATA_FOLDER = "data"
TXT_FILE = "dataset.txt"
CSV_FILE = "stories.csv"
CHUNK_SIZE = 300
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

# -------------------------
# Embedding modeli
# -------------------------
embed_model = SentenceTransformer(EMBEDDING_MODEL)

# -------------------------
# FAISS index ve meta yükle veya oluştur
# -------------------------
INDEX_PATH = "faiss_index.bin"
META_PATH = "index_meta.pkl"

if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    texts = meta["texts"]
else:
    txt_chunks = []
    txt_path = os.path.join(DATA_FOLDER, TXT_FILE)
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        txt_chunks = [raw_text[i:i+CHUNK_SIZE] for i in range(0, len(raw_text), CHUNK_SIZE)]

    csv_chunks = []
    csv_path = os.path.join(DATA_FOLDER, CSV_FILE)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        for content in df['content'].dropna():
            csv_chunks.extend([content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)])

    texts = txt_chunks + csv_chunks
    print(f"Toplam chunk sayısı: {len(texts)}")

    vectors = embed_model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors.astype(np.float32))

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump({"texts": texts}, f)

# -------------------------
# RAG bağlam bulma
# -------------------------
def retrieve_context(query, top_k=TOP_K):
    query_vec = embed_model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vec.astype(np.float32), top_k)
    results = [texts[i] for i in I[0]]
    return "\n".join(results)

# -------------------------
# Groq ile RAG tabanlı cevap
# -------------------------
def ask_groq_rag(query):
    context = retrieve_context(query)
    prompt = f"Bağlam:\n{context}\n\nSoru: {query}\nCevap:"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sen yaratıcı bir yazar asistanısın. Kullanıcının verdiği ana fikirden özgün metin üret."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# -------------------------
# Streamlit Web Arayüzü
# -------------------------
st.set_page_config(
    page_title="Yazar Asistanı Chatbot",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CSS ile tema ve font
# -------------------------
st.markdown("""
<style>
body {
    background-color: #fffaf0;
    font-family: 'Georgia', serif;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Georgia', serif;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📖 Yazar Asistanı 🤖")
st.sidebar.markdown(
    """
    Bu chatbot, veri setlerinden bağlam alarak yaratıcı metinler üretir.
    
    🔹 Ana fikir veya soru yazın  
    🔹 "Gönder" butonuna tıklayın  
    🔹 Üretilen metin altta görünecek
    """
)

# Başlık ve açıklama
st.title("🖋️ Yaratıcı Yazar Asistanı")
st.markdown(
    "Ana fikrinizi veya kısa özetinizi girin, chatbot sizin için **yaratıcı bir metin** üretsin."
)

# Giriş kutusu
query = st.text_area(
    "Ana fikir veya sorunuz:",
    placeholder="Örnek: Kahramanımız gizemli bir ormanda kayboluyor...",
    height=120
)

# Gönder butonu ve cevap gösterimi
answer = None
if st.button("Gönder") and query:
    with st.spinner("Metin üretiliyor..."):
        answer = ask_groq_rag(query)
    st.markdown("**Üretilen Metin:**")
    st.markdown(
        f"""
        <div style="
            background-color:#fff8dc;
            color:#000000;
            padding:15px;
            border-radius:10px;
            line-height:1.5;
        ">
            {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

# Sohbet geçmişi
if 'history' not in st.session_state:
    st.session_state['history'] = []

if query and answer:
    st.session_state['history'].append({"query": query, "answer": answer})

if st.session_state['history']:
    st.markdown("---")
    st.markdown("### 💬 Sohbet Geçmişi (Son 5)")
    for h in reversed(st.session_state['history'][-5:]):
        st.markdown(f"**Soru:** {h['query']}")
        st.markdown(
            f"""
            <div style="
                background-color:#f5f5dc;
                color:#000000;
                padding:10px;
                border-radius:8px;
                line-height:1.5;
            ">
                {h['answer']}
            </div>
            """,
            unsafe_allow_html=True
        )
