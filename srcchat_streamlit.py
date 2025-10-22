import streamlit as st
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import torch

# -------------------------
# .env ve API Key
# -------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# Ayarlar
# -------------------------
INDEX_PATH = "faiss_index.bin"
META_PATH = "index_meta.pkl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

# -------------------------
# Embedding modeli (CPU)
# -------------------------
device = torch.device('cpu')
embed_model = SentenceTransformer(EMBEDDING_MODEL, device=device)

# -------------------------
# FAISS index ve meta yükle
# -------------------------
if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    texts = meta["texts"]
    print(f"FAISS index ve meta dosyaları yüklendi, toplam chunk: {len(texts)}")
else:
    raise FileNotFoundError("FAISS index veya meta dosyası bulunamadı. Lütfen 'faiss_index.bin' ve 'index_meta.pkl' dosyalarını yükleyin.")

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

# CSS ile tema ve font
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
