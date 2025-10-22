🌐 Web Arayüzü & Ürün Kılavuzu
Deploy işlemi tamamlandıktan sonra proje bu linkten erişilebilir olacaktır:
👉 🔗 Chatbot’u Deneyin
<img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/b44a3ed5-4cb8-46ab-b592-fed703a0a3d6" />

Streamlit Deploy Linki : 
https://rag-yazar-chatbot.streamlit.app/

🧠 RAG Yazar Chatbot  
Yazarlar için Akıllı Metin Üretim ve Bilgi Destek Chatbotu
Bu proje, Retrieval-Augmented Generation (RAG) mimarisi kullanarak geliştirilen, Groq destekli bir yazar asistanı chatbotudur.
Chatbot, hem genel bilgi verilerini hem de yazarlıkla ilgili özel veri setlerini kullanarak, bağlama dayalı yaratıcı ve mantıklı metinler üretir.
Özellikle roman, hikâye veya senaryo yazarlarının fikir geliştirme süreçlerinde destek sağlamayı amaçlar.

🎯 Projenin Amacı

Bu proje, yazarlara, içerik üreticilerine ve genel bilgi odaklı kullanıcılara yönelik bir Yapay Zekâ destekli sohbet sistemi geliştirmeyi amaçlamaktadır.
Chatbot, yalnızca genel bilgiyle değil, aynı zamanda özel olarak hazırlanmış yazarlık temalı veri setlerinden beslendiği için kullanıcılara bağlamsal olarak doğru, anlamlı ve özgün yanıtlar sunar.
Sistem, RAG (Retrieval-Augmented Generation) mimarisi üzerine kurulmuştur.
Yani model, cevap üretmeden önce veritabanından en alakalı bilgileri bulur ve bu bağlamı kullanarak yanıt oluşturur.

📦 Veri Seti Hakkında Bilgi

Projede iki tür veri seti kullanılmıştır:
Genel Bilgi Veri Seti
Kaynak: [MuskumPillerum/General-Knowledge](https://huggingface.co/datasets/MuskumPillerum/General-Knowledge)
İçerik: Genel kültür, tarih, bilim, sanat ve günlük yaşam hakkında kısa bilgi kartları.
Yazarlık Odaklı Veri Seti (custom)
Kaynak: Kullanıcı tarafından hazırlanmış özel JSON dosyaları.
İçerik: Yazarlık teknikleri, yaratıcılık ipuçları, hikâye kurgulama ve karakter oluşturma yöntemleri.
Bu iki veri seti, embedding işlemiyle vektör veritabanına aktarılmış ve sorgu sırasında RAG pipeline tarafından kullanılmıştır.

🔹 Çalışma Mantığı
Kullanıcı bir metin veya soru girer.
Sistem, soruyu embedding vektörüne dönüştürür.
FAISS veritabanından en benzer bağlamsal bilgileri bulur.
Bu bağlamlar, LLM modeline prompt olarak eklenir.
Model, RAG tabanlı bir şekilde doğru ve alakalı yanıt üretir.

🧩 Çözüm Mimarisi
A[Kullanıcı Girdisi] --> B[Embedding Oluşturma];
B --> C[FAISS Vektör Veritabanı];
C --> D[İlgili Bilgi Getirme];
D --> E[LLM Modeli (RAG)];
E --> F[Yanıt Üretimi];
F --> G[Gradio Arayüzünde Görüntüleme];


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
5️⃣ Tarayıcıda Görüntüleme
Gradio arayüzü otomatik olarak tarayıcıda açılacaktır.
Eğer açılmazsa terminaldeki localhost linkine tıklayabilirsiniz.





 💬 Kullanım Akışı
Kullanıcı bir soru veya konu yazar.
Sistem, arka planda RAG mimarisiyle bilgi arar.
LLM modeli bağlamsal cevabı üretir.
Yanıt kullanıcıya, sade bir arayüzde gösterilir.


🧠 Örnek Çıktılar
Girdi: “Nasıl daha özgün bir hikâye yazabilirim?”
Yanıt: “Özgünlük için karakterlerinin hedeflerini ve korkularını derinlemesine tanımla.
Farklı bakış açılarından yazmayı dene ve klişelerden kaçın.”
Girdi: “Işık hızı nedir?”
Yanıt: “Işık hızı yaklaşık saniyede 299,792 kilometredir ve evrende bilgi aktarımının en yüksek hız sınırıdır.”


📈 Elde Edilen Sonuçlar
Chatbot, hem genel bilgi hem de yazarlık temelli sorularda anlamlı yanıtlar üretebilmektedir.
RAG pipeline sayesinde model, veri setindeki içeriklerden bağlamsal bilgi çekerek yanıt kalitesini artırmaktadır.
Kullanıcı arayüzü, hızlı yanıt üretimi ve basit etkileşim tasarımı ile işlevseldir.


🧾 Lisans
Bu proje eğitim amaçlı geliştirilmiştir.
Ticari kullanım veya yeniden dağıtım öncesinde geliştirici izni gereklidir.


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








