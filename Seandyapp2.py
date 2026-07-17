"""
Tel-U Jakarta Assistant - Chatbot Virtual Asisten Telkom University Jakarta
Proyek Akhir Pelatihan - Aplikasi Chatbot Sederhana

Cara jalankan:
>>> streamlit run app.py

Catatan:
- Butuh GOOGLE_API_KEY (Gemini API key) untuk berjalan.
- Logo resmi harus berada di assets/telu-jakarta-logo.png (satu folder dengan app.py).
"""

import os
from pathlib import Path

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "telu-jakarta-logo.png"

st.set_page_config(
    page_title="Tel-U Jakarta Assistant",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🎓",
    layout="centered",
)

# ============================================================
# TEMA VISUAL - TELKOM UNIVERSITY (Merah, Maroon, Silver, Abu Tua)
# ============================================================
st.markdown(
    """
    <style>
        :root {
            --tel-red: #E4292C;
            --tel-maroon: #9E1B23;
            --tel-gray: #6D6E71;
            --tel-silver: #B1B3B4;
            --tel-dark: #1A1A1A;
            --tel-bg: #FAFAFA;
        }

        /* Background halaman */
        .stApp {
            background: linear-gradient(180deg, #FAFAFA 0%, #F1F1F1 100%);
        }

        /* Sembunyikan header bawaan streamlit yang polos */
        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* Banner judul */
        .tuj-header {
            background: linear-gradient(120deg, var(--tel-red) 0%, var(--tel-maroon) 100%);
            padding: 1.4rem 1.6rem;
            border-radius: 14px;
            display: flex;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 6px 18px rgba(158, 27, 35, 0.25);
            margin-bottom: 0.6rem;
        }
        .tuj-header img {
            height: 52px;
            background: white;
            padding: 6px 10px;
            border-radius: 8px;
        }
        .tuj-header-text h1 {
            color: white;
            font-size: 1.35rem;
            margin: 0;
            font-weight: 700;
            line-height: 1.25;
        }
        .tuj-header-text p {
            color: #F5D6D6;
            margin: 0;
            font-size: 0.88rem;
        }

        .tuj-tagline {
            text-align: center;
            color: var(--tel-gray);
            font-size: 0.85rem;
            font-style: italic;
            margin: 0.2rem 0 1.2rem 0;
        }

        /* Chat bubble user */
        [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
            background: #F0F0F0;
            border-radius: 14px;
            border: 1px solid #E2E2E2;
        }

        /* Chat bubble AI */
        [data-testid="stChatMessage"]:has(img) {
            background: #FFFFFF;
            border-left: 4px solid var(--tel-red);
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        /* Tombol */
        .stButton > button, .stChatInput button {
            background-color: var(--tel-red) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover {
            background-color: var(--tel-maroon) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A1A1A 0%, #2B2B2B 100%);
        }
        [data-testid="stSidebar"] * {
            color: #F1F1F1 !important;
        }
        [data-testid="stSidebar"] a {
            color: #FF9C9E !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: #444 !important;
        }

        /* Caption footer */
        .tuj-footer {
            text-align: center;
            color: var(--tel-gray);
            font-size: 0.75rem;
            margin-top: 1.5rem;
        }

        /* Kartu logo di sidebar */
        .tuj-sidebar-logo {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 1rem 0.8rem;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            border: 2px solid var(--tel-red);
        }
        .tuj-sidebar-logo img {
            max-width: 100%;
            height: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
if LOGO_PATH.exists():
    import base64

    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    st.markdown(
        f"""
        <div class="tuj-header">
            <img src="data:image/png;base64,{logo_b64}" />
            <div class="tuj-header-text">
                <h1>Tel-U Jakarta Assistant</h1>
                <p>Virtual Assistant Resmi &mdash; Telkom University Jakarta</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.title("Tel-U Jakarta Assistant")

st.markdown(
    '<p class="tuj-tagline">"Contribution To The Nation" &mdash; Tanya seputar kampus, '
    "akademik, dan pendaftaran di Telkom University Jakarta</p>",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR - INFO CEPAT
# ============================================================
with st.sidebar:
    if LOGO_PATH.exists():
        import base64 as _b64

        _sidebar_logo_b64 = _b64.b64encode(LOGO_PATH.read_bytes()).decode()
        st.markdown(
            f"""
            <div class="tuj-sidebar-logo">
                <img src="data:image/png;base64,{_sidebar_logo_b64}" />
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("### 📍 Kampus Tel-U Jakarta")
    st.markdown(
        "- **Daan Mogot** — Jakarta Barat\n"
        "- **Halimun** — Jakarta Selatan\n"
        "- **Minangkabau** — Jakarta Selatan"
    )
    st.markdown("### 🔗 Tautan Resmi")
    st.markdown(
        "- [Website Tel-U Jakarta](https://jakarta.telkomuniversity.ac.id)\n"
        "- [Pendaftaran (SMB)](https://smb.telkomuniversity.ac.id)"
    )
    st.markdown("---")
    st.caption(
        "⚠️ Chatbot ini adalah **prototipe proyek akhir pelatihan**, bukan kanal "
        "resmi Tel-U. Untuk biaya, jadwal, dan syarat pendaftaran terbaru, selalu "
        "cek tautan resmi di atas."
    )

# ============================================================
# API KEY
# ============================================================
# Saat di-deploy ke Streamlit Community Cloud, API key sebaiknya disimpan di
# menu "Secrets" (bukan diketik manual tiap kali). Baris di bawah ini otomatis
# mengambilnya dari st.secrets kalau tersedia; kalau tidak ada (mis. saat run
# lokal tanpa secrets.toml), akan lanjut ke kolom input manual seperti biasa.
if os.environ.get("GOOGLE_API_KEY") is None:
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass  # st.secrets belum dikonfigurasi (wajar saat run lokal) -> lanjut ke input manual

if os.environ.get("GOOGLE_API_KEY") is None:
    st.markdown("**Masukkan API Key Gemini untuk mulai chat**")
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        api_key = st.text_input(
            "API Key",
            type="password",
            label_visibility="collapsed",
            placeholder="Tempel API key Gemini kamu di sini...",
        )
    with col2:
        is_api_key_submitted = st.button("Submit")

    if is_api_key_submitted and api_key != "":
        os.environ["GOOGLE_API_KEY"] = api_key
    if os.environ.get("GOOGLE_API_KEY") is None:
        st.stop()

client = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# Aktifkan Google Search grounding: model bisa mencari info terkini di internet
# secara real-time sebelum menjawab, bukan hanya mengandalkan pengetahuan bawaan
# atau teks yang di-hardcode di SYSTEM_PROMPT di bawah.
# tool_choice="any" memaksa model MELAKUKAN pencarian di setiap giliran jawab,
# bukan menyerahkan keputusan "perlu cari atau tidak" ke model (yang sering kali
# terlalu percaya diri dengan pengetahuan bawaannya dan malah tidak mencari).
SEARCH_GROUNDING_ENABLED = True
if SEARCH_GROUNDING_ENABLED:
    client = client.bind_tools([{"google_search": {}}], tool_choice="any")

# ============================================================
# SYSTEM PROMPT - PENGETAHUAN TEL-U JAKARTA
# ============================================================
# ============================================================
# KNOWLEDGE BASE (dimuat dari file terpisah, mudah diedit tanpa sentuh kode)
# ============================================================
KB_PATH = Path(__file__).parent / "knowledge_base.md"


def load_knowledge_base() -> str:
    if KB_PATH.exists():
        return KB_PATH.read_text(encoding="utf-8")
    return (
        "(knowledge_base.md tidak ditemukan — mohon buat file itu di folder yang "
        "sama dengan app.py agar chatbot punya data kampus.)"
    )


SYSTEM_PROMPT = f"""
Kamu adalah "Tel-U Jakarta Assistant", asisten virtual resmi untuk civitas dan calon
mahasiswa Telkom University Jakarta (Tel-U Jakarta / TUJ). Jawab selalu dalam Bahasa
Indonesia, ramah, sopan, singkat (maksimal 1 paragraf kecuali diminta detail lebih).

=== DATA & FAKTA TENTANG TEL-U JAKARTA (sumber: knowledge_base.md) ===
{load_knowledge_base()}
=== AKHIR DATA ===

ATURAN PENTING:
1. Kamu punya akses tool google_search untuk mencari info real-time. UNTUK PERTANYAAN
   tentang hal berikut, kamu WAJIB memanggil tool google_search terlebih dahulu sebelum
   menjawab — JANGAN langsung menjawab dari ringkasan umum di bagian PROFIL di atas:
   - Daftar/nama program studi yang tersedia
   - Biaya kuliah (UP3, SDP2, BPP, atau nominal apa pun)
   - Jadwal pendaftaran, jalur seleksi yang sedang dibuka, dan deadline-nya
   - Info beasiswa yang sedang aktif beserta syaratnya
   - Berita atau kegiatan kampus terbaru
   Setelah dapat hasil pencarian, jawab berdasarkan hasil itu (boleh sebutkan sumbernya
   kalau ada). Kalau hasil pencarian tetap tidak jelas/tidak ditemukan, baru katakan
   jujur dan arahkan ke jakarta.telkomuniversity.ac.id atau smb.telkomuniversity.ac.id.
   Untuk keputusan penting (bayar biaya, deadline daftar), tetap tambahkan imbauan
   singkat untuk konfirmasi ulang ke sumber resmi karena info bisa berubah sewaktu-waktu.
2. Jika kamu tidak yakin atau tidak punya data tentang sesuatu, jangan mengarang. Katakan
   dengan jujur bahwa kamu tidak punya info pasti dan arahkan ke kontak resmi kampus atau
   bagian admisi/PMB.
3. Kamu boleh membantu topik umum seputar kehidupan kampus, tips akademik, atau pertanyaan
   ringan lain, tapi selalu jaga identitasmu sebagai asisten Tel-U Jakarta.
4. Jangan pernah mengaku sebagai manusia atau staf resmi kampus — kamu adalah asisten AI.
"""

# ============================================================
# CHAT HISTORY & INTERAKSI
# ============================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [SystemMessage(SYSTEM_PROMPT)]

ai_avatar = str(LOGO_PATH) if LOGO_PATH.exists() else "🎓"

for chat in st.session_state["chat_history"]:
    if type(chat) is SystemMessage:
        continue
    elif type(chat) is HumanMessage:
        role, avatar = "User", "🧑"
    elif type(chat) is AIMessage:
        role, avatar = "AI", ai_avatar
    with st.chat_message(role, avatar=avatar):
        st.markdown(chat.text)

user_prompt = st.chat_input("Tanya seputar Tel-U Jakarta...")
if not user_prompt:
    st.markdown(
        '<p class="tuj-footer">Prototipe proyek akhir pelatihan chatbot &mdash; '
        "bukan kanal informasi resmi Telkom University Jakarta</p>",
        unsafe_allow_html=True,
    )
    st.stop()

st.session_state["chat_history"].append(HumanMessage(user_prompt))

with st.chat_message("User", avatar="🧑"):
    st.markdown(user_prompt)

try:
    response = client.invoke(st.session_state["chat_history"])
except Exception as e:
    error_text = str(e)
    if "API_KEY_INVALID" in error_text or "API key not valid" in error_text:
        friendly_msg = (
            "⚠️ **API Key tidak valid.** Sepertinya Gemini API key yang dipakai "
            "salah atau sudah tidak aktif. Silakan buat/verifikasi key baru di "
            "[Google AI Studio](https://aistudio.google.com/apikey), lalu restart "
            "aplikasi ini sepenuhnya (stop & jalankan ulang `streamlit run`) "
            "sebelum mencoba lagi."
        )
    else:
        friendly_msg = (
            "⚠️ Terjadi kendala saat menghubungi model AI. Silakan coba lagi "
            "sebentar lagi. Detail teknis: `" + error_text[:200] + "`"
        )
    # Buang pesan user yang gagal diproses supaya tidak nyangkut di history
    st.session_state["chat_history"].pop()
    with st.chat_message("AI", avatar=ai_avatar):
        st.markdown(friendly_msg)
    st.stop()

st.session_state["chat_history"].append(response)

with st.chat_message("AI", avatar=ai_avatar):
    st.markdown(response.text)
