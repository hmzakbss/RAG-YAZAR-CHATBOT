🧠 RAG Yazar Chatbot
Yazarlar için Akıllı Metin Üretim ve Bilgi Destek Chatbotu
Bu proje, Retrieval-Augmented Generation (RAG) mimarisi kullanarak geliştirilen, Groq destekli bir yazar asistanı chatbotudur.
Chatbot, hem genel bilgi verilerini hem de yazarlıkla ilgili özel veri setlerini kullanarak, bağlama dayalı yaratıcı ve mantıklı metinler üretir.
Özellikle roman, hikâye veya senaryo yazarlarının fikir geliştirme süreçlerinde destek sağlamayı amaçlar.


🚀 Özellikler
Groq API (LLaMA 3.3 70B) modeliyle güçlü dil üretimi
FAISS vektör veritabanı ile hızlı ve etkili bilgi geri çağırma
SentenceTransformer (all-MiniLM-L6-v2) modeliyle metin gömme (embedding) işlemi
RAG pipeline: Hem genel bilgilerden hem de kullanıcı veri setlerinden bağlam toplayarak cevap üretme
Streamlit arayüzü: Kullanıcı dostu, modern ve sade web tabanlı sohbet ekranı
Çoklu veri desteği: Hem .txt hem .csv formatındaki veri setlerini okuyabilme
Yazar odaklı özel eğitim verileri (hikaye taslağı, ana fikir, karakter gelişimi gibi)


🧩 Kullanılan Teknolojiler
| Bileşen                    | Teknoloji                                |
| -------------------------- | ---------------------------------------- |
| **Embedding Model**        | `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector Database**        | `FAISS`                                  |
| **Generation Model**       | `Groq - LLaMA 3.3 70B Versatile`         |
| **RAG Pipeline Framework** | Custom (manuel RAG yapısı)               |
| **Frontend**               | Streamlit                                |
| **Dil**                    | Python 3.10+                             |


⚙️ Kurulum
1️⃣ Sanal ortam oluştur
python -m venv .venv
.\.venv\Scripts\activate
2️⃣ Gerekli paketleri yükle
pip install -r requirements.txt
3️⃣ .env dosyasını oluştur
Ana dizinde .env adında bir dosya oluştur ve Groq API anahtarını ekle:
GROQ_API_KEY=your_api_key_here
5️⃣ Uygulamayı başlat
streamlit run src/chat.py


💬 Kullanım
Uygulama açıldığında sohbet ekranına soru veya hikaye fikrini yaz.
Chatbot, önce veri setlerinden bağlam bulur.
Groq modeli, bu bağlamı kullanarak anlamlı bir cevap veya metin üretir.
💡 Örnek:
“Bir bilim kurgu romanı için ilginç bir başlangıç fikri üret.”
💬 Chatbot: “Yıl 2145. İnsanlık, yapay zekâlarla birlikte yaşamanın dengesini kaybetmiştir…”

🔐 Güvenlik
API anahtarı kod içinde tutulmaz → .env dosyasında saklanır
.gitignore dosyası ile .env, venv, __pycache__ gibi dosyalar GitHub’a yüklenmez

🧠 Gelecek Geliştirmeler
LlamaIndex veya LangChain entegrasyonu
Kullanıcıdan alınan yeni verilerle dinamik vektör veritabanı güncelleme
Yazar türüne (roman, senaryo, kısa hikâye) göre özel yanıt üretimi
Chat geçmişi ve oturum kaydı desteği


👨‍💻 Geliştiriciler
Hamza Akbaş
🎓 Sakarya Üniversitesi — Bilişim Sistemleri Mühendisliği
İclal Aydın
🎓Çukurova Üniversitesi - Matematik

