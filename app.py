from pathlib import Path
import re
import streamlit as st

st.set_page_config(page_title="AI Tutor Bahasa Indonesia | Teks Berita", page_icon="📰", layout="wide")

# Tema visual: ruang redaksi digital untuk pembelajaran teks berita
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
:root { --navy:#102f55; --blue:#2563eb; --sky:#eaf5ff; --gold:#ffbf3f; --ink:#17365d; }
html, body, [class*="css"] { font-family:'Poppins', sans-serif; }
.stApp { background: linear-gradient(135deg,#f3f8ff 0%,#ffffff 50%,#fff8e9 100%); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(255,255,255,.78); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#102f55 0%,#174a7e 70%,#0c2340 100%); }
[data-testid="stSidebar"] * { color:#f6fbff !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.12); padding:10px 12px; border-radius:12px; margin:5px 0; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,191,63,.20); }
.block-container { padding-top:1.7rem; padding-bottom:2.5rem; max-width:1400px; }
h1 { color:#12345a !important; font-weight:800 !important; letter-spacing:-.7px; }
h2,h3 { color:#173f70 !important; font-weight:700 !important; }
[data-testid="stMetric"] { background:white; border:1px solid #d8e8fb; border-radius:16px; padding:16px 18px; box-shadow:0 5px 18px rgba(25,72,125,.06); }
[data-testid="stExpander"] { background:rgba(255,255,255,.92); border:1px solid #d8e8fb; border-radius:14px; margin-bottom:9px; }
.stButton>button, .stFormSubmitButton>button { border:0; border-radius:12px; font-weight:700; background:linear-gradient(90deg,#2563eb,#3b82f6); color:white; padding:.65rem 1.1rem; box-shadow:0 5px 12px rgba(37,99,235,.18); }
.stButton>button:hover, .stFormSubmitButton>button:hover { background:linear-gradient(90deg,#1747b5,#2563eb); color:white; border:0; }
div[data-testid="stAlert"] { border-radius:14px; }
.hero-news { background:linear-gradient(110deg,#e3f2ff 0%,#f6fbff 58%,#fff0c5 100%); border:1px solid #cfe4fb; border-radius:22px; padding:28px 30px; margin-bottom:20px; position:relative; overflow:hidden; box-shadow:0 10px 30px rgba(28,73,125,.08); }
.hero-news h2 { margin:0 0 8px 0; color:#102f55 !important; font-size:30px; }
.hero-news p { margin:0; font-size:15px; line-height:1.7; max-width:800px; }
.hero-kicker { color:#2563eb; font-size:12px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.section-label { background:#eaf3ff; color:#1d4f91; border-left:5px solid #ffbf3f; border-radius:8px; padding:10px 14px; font-weight:700; margin:18px 0 12px; }
.feature-card { min-height:190px; padding:19px; border-radius:17px; border:1px solid #d8e6f7; background:#fff; box-shadow:0 7px 20px rgba(23,63,112,.06); margin-bottom:10px; }
.feature-card .emoji { font-size:29px; margin-bottom:8px; }
.feature-card h4 { margin:0 0 7px; color:#163e70; font-size:16px; }
.feature-card p { color:#526984; font-size:13px; line-height:1.6; margin:0; }
.quote-card { background:#fff4d7; border:1px solid #ffdf8b; border-radius:17px; padding:18px; color:#694a0b; font-style:italic; }
.mini-tag { display:inline-block; background:#dbeafe; color:#1d4ed8; border-radius:99px; padding:5px 10px; font-size:12px; font-weight:700; margin:3px 4px 3px 0; }
hr { border-color:#dce9f7 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# KONFIGURASI DAN MATERI
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"

CP = "Peserta didik mampu menulis gagasan, pikiran, pandangan, dan pengetahuan metakognisi untuk berbagai tujuan secara logis, kritis, dan kreatif. Peserta didik mampu menulis teks berita sesuai ketentuan yang telah dipelajari."
ATP = [
    "Membaca berbagai tipe teks nonfiksi dan fiksi di media cetak maupun elektronik.",
    "Mengevaluasi informasi berita dengan memperhatikan fakta, sumber, dan objektivitas.",
    "Menulis gagasan dan informasi secara logis, kritis, dan kreatif.",
    "Menyusun teks berita berdasarkan unsur 5W+1H dan struktur berita.",
    "Menyajikan hasil karya berita dengan bahasa yang jelas, santun, dan sesuai kaidah."
]
TUJUAN = [
    "Mengidentifikasi unsur 5W+1H dan struktur teks berita.",
    "Menganalisis informasi aktual dan akurat dari sumber berita.",
    "Membedakan fakta, opini, dan klaim yang belum terverifikasi.",
    "Merancang teks berita dengan struktur dan unsur yang tepat.",
    "Menyunting teks berita agar objektif, jelas, dan menggunakan ejaan yang baik."
]

MATERI = {
"1. Pengertian Teks Berita": """Teks berita adalah teks yang menyampaikan informasi mengenai peristiwa nyata kepada masyarakat. Informasi berita harus berdasarkan fakta dan sumber yang dapat diperiksa, bukan hasil khayalan atau dugaan penulis. Berita dapat ditemukan di surat kabar, majalah, radio, televisi, situs berita, dan media sosial.

Berita membantu masyarakat mengetahui peristiwa yang tidak disaksikan secara langsung. Berita yang baik menyampaikan informasi secara jelas, lengkap, relevan, dan dapat dipertanggungjawabkan. Penulis harus memisahkan fakta dari pendapat pribadi dan tidak melebih-lebihkan peristiwa.""",
"2. Fungsi dan Tujuan Teks Berita": """Teks berita berfungsi menyampaikan informasi, menambah pengetahuan, membantu masyarakat memahami peristiwa, serta mendukung pengambilan keputusan. Berita juga dapat melatih pembaca berpikir kritis karena pembaca perlu memeriksa sumber, data, konteks, dan pernyataan narasumber.

Dalam pembelajaran, teks berita melatih peserta didik mengumpulkan informasi, melakukan wawancara, mencatat data, memilih informasi penting, lalu menyusunnya menjadi tulisan yang mudah dipahami.""",
"3. Ciri-Ciri Teks Berita": """1. Faktual: berlandaskan peristiwa atau data yang dapat dibuktikan.
2. Aktual: berkaitan dengan peristiwa baru atau perkembangan yang masih penting.
3. Objektif: tidak dipengaruhi penilaian pribadi penulis.
4. Jelas dan ringkas: menggunakan bahasa yang mudah dipahami serta langsung pada pokok peristiwa.
5. Memiliki sumber: informasi dapat ditelusuri kepada saksi, narasumber, dokumen, atau data yang relevan.
6. Relevan: memiliki nilai penting bagi pembaca atau masyarakat.""",
"4. Unsur Berita 5W+1H": """What (apa): peristiwa yang terjadi.
Who (siapa): orang atau pihak yang terlibat.
Where (di mana): lokasi peristiwa.
When (kapan): waktu peristiwa.
Why (mengapa): penyebab, latar belakang, atau alasan yang didukung informasi.
How (bagaimana): proses, kronologi, atau dampak peristiwa.

Tidak semua unsur harus berada dalam satu kalimat. Namun, berita perlu menyajikan informasi yang cukup agar pembaca memahami inti peristiwa. Hindari menyajikan dugaan sebagai penyebab yang sudah pasti.""",
"5. Struktur Teks Berita": """Judul berita: menggambarkan pokok peristiwa secara singkat, jelas, dan sesuai isi. Judul tidak boleh menyesatkan atau menggunakan sensasi yang tidak didukung fakta.

Teras/kepala berita: bagian awal yang menyampaikan informasi terpenting. Teras biasanya memuat sebagian unsur 5W+1H sehingga pembaca segera memahami inti peristiwa.

Tubuh/leher berita: mengembangkan informasi pada teras, misalnya kronologi, data, latar belakang, kutipan narasumber, dan penjelasan tambahan.

Ekor berita: memuat informasi tambahan yang tingkat kepentingannya lebih rendah. Dalam pola piramida terbalik, informasi terpenting ditempatkan lebih dahulu, kemudian diikuti rincian tambahan.""",
"6. Fakta dan Opini": """Fakta adalah informasi yang dapat diperiksa kebenarannya, misalnya waktu, tempat, angka, nama, hasil pengamatan, dokumen, atau peristiwa yang benar-benar terjadi. Opini adalah penilaian atau pendapat yang belum tentu dapat dibuktikan sebagai kebenaran objektif.

Contoh fakta: “Sebanyak 120 siswa mengikuti kegiatan literasi pada Senin pagi.” Pernyataan ini dapat diperiksa melalui daftar peserta dan waktu kegiatan.

Contoh opini: “Kegiatan literasi itu merupakan kegiatan paling hebat.” Kata “paling hebat” menunjukkan penilaian. Opini narasumber dapat dimuat sebagai kutipan jika sumbernya jelas, tetapi jangan menyajikannya seolah-olah fakta yang telah terverifikasi.""",
"7. Kaidah Kebahasaan": """Teks berita menggunakan bahasa baku, lugas, jelas, dan tidak menghakimi. Unsur kebahasaan yang sering digunakan meliputi:
- kata kerja tindakan, misalnya mengadakan, meninjau, mengikuti, dan menyampaikan;
- keterangan waktu dan tempat untuk menjelaskan kapan dan di mana peristiwa terjadi;
- konjungsi temporal, misalnya kemudian, setelah itu, sebelumnya, selanjutnya, dan akhirnya;
- kalimat langsung untuk mengutip ucapan narasumber;
- kalimat tidak langsung untuk menyampaikan kembali informasi narasumber;
- kata yang netral dan tidak berlebihan.

Judul harus sesuai dengan isi berita. Hindari kata sensasional seperti “mengerikan” atau “hancur lebur” apabila kata tersebut membesar-besarkan kejadian.""",
"8. Memeriksa Akurasi dan Kelayakan Berita": """Sebelum menerbitkan berita, periksa asal sumber, tanggal publikasi, identitas narasumber, bukti atau data pendukung, dan kesesuaian judul dengan isi. Bandingkan informasi penting dengan sumber tepercaya lain jika memungkinkan. Bedakan fakta, opini narasumber, dan klaim yang belum terbukti.

Jangan langsung menyebarkan informasi hanya karena viral atau dikirim oleh orang yang dikenal. Baca berita secara utuh dan periksa konteksnya. Jika informasi belum terkonfirmasi, tuliskan secara hati-hati atau jangan menyajikannya sebagai fakta.""",
"9. Langkah Menulis Teks Berita": """1. Menentukan peristiwa yang aktual dan layak diberitakan.
2. Mengumpulkan informasi melalui pengamatan, wawancara, dokumen, dan sumber tepercaya.
3. Mencatat unsur 5W+1H.
4. Memeriksa kebenaran data dan membedakan fakta dari opini.
5. Menyusun kerangka berdasarkan struktur judul, teras, tubuh, dan ekor berita.
6. Menulis dengan bahasa baku, jelas, ringkas, dan objektif.
7. Memeriksa ejaan, tanda baca, kutipan, sumber, dan kesesuaian judul.
8. Meminta umpan balik, merevisi, lalu menyajikan berita.""",
"10. Contoh Teks Berita": """**Siswa SMA Gelar Aksi Bersih Lingkungan Sekolah**

Medan, Jumat — Siswa kelas XI SMA Harapan mengadakan kegiatan bersih lingkungan di halaman sekolah pada Jumat pagi. Kegiatan tersebut diikuti oleh siswa, guru, dan pengurus OSIS.

Para peserta membersihkan taman, memilah sampah, dan mengumpulkan daun kering. Menurut ketua panitia, kegiatan ini dilakukan untuk meningkatkan kepedulian warga sekolah terhadap kebersihan lingkungan. Pihak sekolah menyampaikan bahwa sampah yang terkumpul akan dipilah sebelum dibuang.

Kegiatan berakhir menjelang siang. Panitia berencana mengadakan kegiatan serupa secara berkala. Contoh ini bersifat ilustratif; apabila digunakan sebagai berita nyata, nama, waktu, jumlah, dan kutipan harus diverifikasi terlebih dahulu.

**Analisis singkat:** What: kegiatan bersih lingkungan; Who: siswa, guru, OSIS; Where: SMA Harapan, Medan; When: Jumat pagi; Why: meningkatkan kepedulian; How: membersihkan taman dan memilah sampah."""
}

SOAL = [
 {"q":"Kutipan: ‘Terjadi antrean panjang sejauh dua kilometer di gerbang tol pada Minggu sore. Kemacetan ini diduga karena sistem pembayaran elektronik mengalami gangguan.’ Unsur yang belum terjawab secara pasti dan faktual adalah …", "opts":["What (apa)","When (kapan)","Where (di mana)","Why (mengapa)","Who (siapa)"],"key":3,"why":"Penyebab masih dinyatakan sebagai dugaan melalui kata ‘diduga’, sehingga unsur Why belum pasti."},
 {"q":"Kesalahan utama teras berita yang menyebut kegiatan sekolah ‘sangat luar biasa, spektakuler, dan paling tidak terlupakan’ adalah …", "opts":["Tidak memuat waktu dan tempat","Melanggar objektivitas karena memakai penilaian pribadi","Bahasanya terlalu kaku","Tidak ada kutipan langsung","Informasi penting selalu harus di akhir"],"key":1,"why":"Ungkapan tersebut berupa penilaian subjektif, bukan penyampaian informasi secara objektif."},
 {"q":"Perhatikan kalimat: (1) ‘Kegiatan ini merupakan program terbaik tahun ini.’ (2) Kepala sekolah menilai, ‘Kegiatan ini merupakan program terbaik tahun ini.’ Analisis paling tepat adalah …", "opts":["Keduanya fakta","Kalimat (1) merupakan penilaian penulis, sedangkan (2) menandai opini sebagai pernyataan narasumber","Keduanya fakta karena kegiatan terjadi","Kalimat (2) pasti opini penulis","Semua opini harus dihapus"],"key":1,"why":"Pernyataan kedua jelas mengatribusikan penilaian kepada kepala sekolah; sumber opini ditandai."},
 {"q":"Mengapa ekor berita biasanya dapat dipotong lebih dahulu ketika ruang publikasi terbatas?", "opts":["Berisi simpulan yang sama dengan judul","Hanya berisi opini penulis","Berisi rincian tambahan sehingga pemotongannya tidak merusak inti informasi","Paling sulit dipahami","Selalu memuat How yang bertele-tele"],"key":2,"why":"Dalam pola piramida terbalik, ekor memuat informasi tambahan yang kepentingannya lebih rendah."},
 {"q":"Judul ‘Mengerikan! Sekolah Hancur Diserang Ribuan Massa!’ ternyata berisi berita kerja bakti merobohkan gudang tua. Pelanggaran utamanya adalah …", "opts":["Memakai tanda seru","Judul menyesatkan dan melebih-lebihkan fakta","Berita kurang aktual","Tidak ada unsur Why di judul","Kerja bakti tidak boleh diberitakan"],"key":1,"why":"Judul tidak sesuai dengan isi dan membangun kesan peristiwa yang keliru."},
 {"q":"Jika tubuh berita memuat klaim tanpa pernyataan narasumber atau data pendukung, tindakan paling tepat adalah …", "opts":["Menganggapnya ekor berita","Memercayainya karena ada di media sosial","Menganggapnya fakta karena telah diterbitkan","Menandainya sebagai klaim yang belum terverifikasi dan memeriksa sumbernya","Menambahkan opini pribadi"],"key":3,"why":"Klaim tanpa bukti perlu diverifikasi dan tidak boleh langsung dinyatakan sebagai fakta."},
 {"q":"Kata ‘setelah’, ‘kemudian’, dan ‘selanjutnya’ terutama berfungsi untuk …", "opts":["Memisahkan kalimat langsung","Menunjukkan urutan kronologi atau hubungan temporal","Menjelaskan tempat","Memisahkan fakta dan opini","Menegaskan judul"],"key":1,"why":"Kata tersebut merupakan penanda waktu yang membantu pembaca memahami kronologi."},
 {"q":"Siswa hanya mencatat nama pemenang, waktu, dan tempat perlombaan lalu langsung menerbitkan berita. Kekurangan utamanya adalah …", "opts":["Berita tidak aktual","Tidak ada opini siswa","Pembaca tidak memperoleh gambaran utuh karena alasan dan proses peristiwa belum dijelaskan","Tidak ada kalimat langsung sehingga berita tidak sah","Struktur berita otomatis terbalik"],"key":2,"why":"Informasi tentang alasan dan proses/dampak (Why dan How) dapat diperlukan untuk memahami peristiwa secara utuh."},
 {"q":"Data: gempa magnitudo 5,2; warga pesisir; Kabupaten Bantul; Jumat pagi; beberapa bangunan retak dan tidak ada korban jiwa. Teras berita paling proporsional adalah …", "opts":["Pergeseran lempeng menyebabkan bangunan retak dan warga panik pada Jumat pagi.","Gempa bermagnitudo 5,2 mengguncang Kabupaten Bantul pada Jumat pagi dan membuat warga pesisir berhamburan keluar rumah.","Gempa tidak menimbulkan korban jiwa tetapi warga harus waspada terhadap gempa susulan.","Pergeseran lempeng menyebabkan gempa yang sangat mengerikan.","Warga berhamburan keluar rumah tanpa korban jiwa setelah pergeseran lempeng."],"key":1,"why":"Pilihan B paling ringkas menyampaikan peristiwa, lokasi, waktu, dan dampak secara netral."},
 {"q":"Saat menerima tautan berita di grup chat, tindakan berpikir kritis yang paling tepat adalah …", "opts":["Langsung membagikan agar cepat tersebar","Membaca judul saja","Memeriksa sumber, membaca isi lengkap, dan mengecek fakta serta pernyataan narasumber","Mencari ekor berita untuk mengetahui sikap penulis","Menghafalkan 5W+1H tanpa memeriksa sumber"],"key":2,"why":"Verifikasi sumber dan isi secara utuh membantu mencegah penyebaran informasi keliru."}
]

# =========================================================
# FUNGSI PENDUKUNG
# =========================================================
def load_database():
    docs = []
    if DB_DIR.exists():
        for file in sorted(DB_DIR.glob("*.txt")):
            try:
                text = file.read_text(encoding="utf-8")
                if text.strip(): docs.append((file.name, text))
            except Exception:
                continue
    return docs

def normalize(text):
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).split()

def retrieve_answer(question, docs):
    q_tokens = set(normalize(question))
    if not q_tokens:
        return None, None
    stop = {"apa","itu","yang","dan","di","ke","dari","dengan","bagaimana","jelaskan","tolong","saya","untuk","dalam","adalah","sebutkan","ya"}
    q_tokens -= stop
    candidates = []
    for name, body in docs:
        tokens = set(normalize(body))
        score = len(q_tokens & tokens) / max(1, len(q_tokens))
        if score > 0:
            candidates.append((score, name, body))
    if not candidates:
        return None, None
    candidates.sort(reverse=True, key=lambda x: x[0])
    score, name, body = candidates[0]
    if score < 0.12:
        return None, None
    # Pilih paragraf paling relevan secara sederhana
    paragraphs = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]
    ranked = []
    for para in paragraphs:
        toks = set(normalize(para))
        s = len(q_tokens & toks) / max(1, len(q_tokens))
        ranked.append((s, para))
    ranked.sort(reverse=True, key=lambda x: x[0])
    answer = "\n\n".join(p for s, p in ranked[:2] if s > 0)
    if not answer:
        answer = body[:1800]
    return answer, name

# =========================================================
# SIDEBAR / NAVIGASI
# =========================================================
st.sidebar.title("📰 AI Tutor Bahasa Indonesia")
st.sidebar.caption("Pembelajaran Teks Berita · Kelas XI")
st.sidebar.markdown("<div style='padding:8px 2px 18px;text-align:center'><div style='font-size:44px'>📰</div><div style='font-size:22px;font-weight:800;line-height:1.2'>AI TUTOR<br>TEKS BERITA</div><div style='font-size:11px;opacity:.8;margin-top:8px'>BELAJAR · PAHAMI · TULIS</div></div>", unsafe_allow_html=True)
st.sidebar.markdown("### 👥 Pilih Ruang Akses")
role = st.sidebar.radio("Masuk sebagai", ["Siswa", "Guru"], format_func=lambda x: "🎒 Siswa" if x == "Siswa" else "🧑‍🏫 Guru", key="user_role")
student_pages = ["Beranda", "Petunjuk Penggunaan", "Materi", "Evaluasi", "Rubrik Penilaian"]
teacher_pages = ["Beranda Guru", "Perangkat Ajar", "Bank Soal", "Rubrik Penilaian Guru", "Petunjuk Guru"]
page_labels = {
    "Beranda":"🏠  Beranda", "Petunjuk Penggunaan":"📖  Petunjuk Penggunaan", "Materi":"🗞️  Materi", "Evaluasi":"📝  Evaluasi", "Rubrik Penilaian":"🏆  Rubrik Penilaian",
    "Beranda Guru":"🧑‍🏫  Beranda Guru", "Perangkat Ajar":"📚  Perangkat Ajar", "Bank Soal":"📝  Bank Soal & Evaluasi", "Rubrik Penilaian Guru":"📊  Rubrik & Penilaian", "Petunjuk Guru":"🧭  Petunjuk Guru"
}
page_options = student_pages if role == "Siswa" else teacher_pages
page = st.sidebar.radio("🧭 MENU " + ("SISWA" if role == "Siswa" else "GURU"), page_options, format_func=lambda x: page_labels[x], key=f"nav_{role}")
st.sidebar.divider()
if role == "Guru":
    st.sidebar.caption("🛠️ Ruang pengelolaan pembelajaran. Perubahan dan hasil siswa belum tersimpan ke basis data bersama.")
else:
    st.sidebar.caption("✨ Belajar, berlatih, dan periksa kembali fakta sebelum membagikan berita.")

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "chat" not in st.session_state:
    st.session_state.chat = []

if page == "Beranda Guru":
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🧑‍🏫 TEACHER CONTROL ROOM · DIGITAL NEWSROOM</div><h2>👋 Selamat datang, Bapak/Ibu Guru!</h2><p>Kelola perangkat ajar, tinjau bank soal, dan gunakan rubrik untuk memandu pembelajaran teks berita. Desain ruang guru tetap menggunakan tema biru-jurnalistik dengan aksen kuning keemasan.</p><div style='margin-top:15px'><span class='mini-tag'>📚 Perangkat Ajar</span><span class='mini-tag'>📝 Bank Soal</span><span class='mini-tag'>📊 Penilaian</span></div></div>", unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("📚 Topik materi", len(MATERI), "Siap ditinjau")
    b.metric("📝 Butir soal", len(SOAL), "Pilihan ganda")
    c.metric("🎯 Skor maksimal", "100", "10 poin per jawaban benar")
    st.markdown("<div class='section-label'>🧰 PINTASAN GURU</div>", unsafe_allow_html=True)
    cols = st.columns(4)
    teacher_cards = [("📚","Perangkat Ajar","Tinjau CP, ATP, tujuan, dan materi."),("📝","Bank Soal","Periksa butir soal dan kunci jawaban."),("📊","Rubrik Penilaian","Gunakan rubrik untuk evaluasi dan proyek berita."),("🧭","Petunjuk Guru","Ketahui batasan dan alur penggunaan aplikasi.")]
    for col,(emoji,title,desc) in zip(cols,teacher_cards):
        with col: st.markdown(f"<div class='feature-card'><div class='emoji'>{emoji}</div><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>📌 CATATAN PENGELOLAAN</div>", unsafe_allow_html=True)
    st.info("Halaman guru membantu meninjau bahan ajar dan instrumen penilaian. Saat ini aplikasi belum memiliki login terverifikasi, penyimpanan nilai siswa lintas perangkat, atau basis data kelas. Jangan gunakan pilihan peran sebagai pengamanan data rahasia.")
    with st.expander("🛤️ Alur pembelajaran yang disarankan"):
        st.markdown("1. Tinjau CP, ATP, dan tujuan pembelajaran.\n2. Sesuaikan materi dengan perangkat ajar yang digunakan di kelas.\n3. Periksa butir soal dan kunci pada Bank Soal.\n4. Jelaskan kriteria keberhasilan melalui rubrik.\n5. Minta siswa mengerjakan evaluasi secara mandiri dan bahas hasilnya.")

elif page == "Perangkat Ajar":
    st.title("📚 Perangkat Ajar Teks Berita")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🗂️ TEACHING KIT</div><h2>Rencanakan pembelajaran yang terarah</h2><p>Tinjau capaian, alur tujuan, tujuan pembelajaran, serta materi yang tersedia pada aplikasi.</p></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("🎯 Capaian Pembelajaran (CP)")
        st.write(CP)
    with st.container(border=True):
        st.subheader("🛤️ Alur Tujuan Pembelajaran (ATP)")
        for i,item in enumerate(ATP,1): st.markdown(f"**{i}.** {item}")
    with st.container(border=True):
        st.subheader("✅ Tujuan Pembelajaran")
        for item in TUJUAN: st.markdown(f"- {item}")
    st.markdown("<div class='section-label'>🗞️ DAFTAR MATERI</div>", unsafe_allow_html=True)
    for title,body in MATERI.items():
        with st.expander(title): st.markdown(body)
    st.warning("Sebelum digunakan untuk penilaian resmi, cocokkan kembali redaksi CP dan ATP dengan dokumen perangkat ajar final dari dosen/guru pembimbing.")

elif page == "Bank Soal":
    st.title("📝 Bank Soal & Evaluasi")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🔐 TEACHER REVIEW</div><h2>Tinjau instrumen evaluasi</h2><p>Periksa pertanyaan, opsi, kunci jawaban, dan alasan sebelum evaluasi digunakan oleh siswa.</p></div>", unsafe_allow_html=True)
    st.caption("Tampilan ini untuk peninjauan guru. Kunci jawaban ditampilkan karena halaman ini berada di ruang guru.")
    for i,q in enumerate(SOAL,1):
        with st.expander(f"Soal {i} · {q['q'][:95]}{'…' if len(q['q'])>95 else ''}"):
            st.markdown(f"**Pertanyaan:** {q['q']}")
            for j,opt in enumerate(q['opts']):
                st.markdown(f"{'✅' if j == q['key'] else '▫️'} {chr(65+j)}. {opt}")
            st.info(f"**Kunci:** {chr(65+q['key'])}. {q['opts'][q['key']]}\n\n**Pembahasan:** {q['why']}")
    st.download_button("⬇️ Unduh kisi-kisi ringkas (CSV)", data="Nomor,Indikator\n" + "\n".join(f"{i},Teks berita: pemahaman konsep dan berpikir kritis" for i in range(1,len(SOAL)+1)), file_name="kisi_kisi_teks_berita.csv", mime="text/csv")

elif page == "Rubrik Penilaian Guru":
    st.title("📊 Rubrik & Penilaian Guru")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🏆 ASSESSMENT STUDIO</div><h2>Penilaian yang transparan dan terarah</h2><p>Gunakan kriteria berikut sebagai acuan saat memeriksa evaluasi dan proyek menulis teks berita.</p></div>", unsafe_allow_html=True)
    st.subheader("📝 Skema evaluasi pilihan ganda")
    x,y = st.columns(2)
    x.metric("Jumlah soal", len(SOAL))
    y.metric("Bobot per jawaban benar", "10 poin")
    st.latex(r"\text{Nilai} = \frac{\text{jawaban benar}}{10} \times 100")
    st.markdown("### 📈 Penyesuaian batas kategori")
    passing = st.slider("Ambang ketercapaian / KKTP (contoh awal)", min_value=50, max_value=100, value=75, step=5)
    st.info(f"Ambang yang dipilih pada sesi ini: **{passing}**. Nilai ini hanya pengaturan sementara di sesi aplikasi dan belum disimpan permanen.")
    st.markdown("### 🧾 Rubrik proyek menulis teks berita")
    st.write("Gunakan skala 1–4 untuk setiap aspek, lalu diskusikan umpan balik secara spesifik dengan siswa.")
    st.table({"Aspek":["Kelengkapan 5W+1H","Struktur berita","Fakta dan akurasi sumber","Objektivitas dan bahasa","Ejaan dan penyajian"],"4 — Sangat Baik":["Unsur lengkap dan jelas","Judul, teras, tubuh, ekor tersusun efektif","Fakta kuat dan sumber dapat diperiksa","Netral, lugas, tidak menyesatkan","Hampir tanpa kesalahan; penyajian sangat jelas"],"3 — Baik":["Sebagian besar unsur lengkap","Struktur jelas dengan kekurangan kecil","Sebagian besar informasi didukung sumber","Cukup objektif dan jelas","Ada sedikit kesalahan"],"2 — Cukup":["Beberapa unsur penting hilang","Struktur kurang seimbang","Sebagian klaim belum didukung","Masih ada opini atau kata berlebihan","Kesalahan cukup mengganggu"],"1 — Perlu Bimbingan":["Banyak unsur tidak tersedia","Struktur sulit dikenali","Sumber tidak jelas atau informasi meragukan","Bahasa subjektif/menyesatkan","Banyak kesalahan yang mengganggu pemahaman"]})
    st.warning("Aplikasi belum merekap nilai banyak siswa atau menyimpan hasil ke database. Untuk rekap kelas, diperlukan fitur penyimpanan nilai dan identitas siswa yang dirancang dengan perlindungan data.")

elif page == "Petunjuk Guru":
    st.title("🧭 Petunjuk Penggunaan untuk Guru")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>👩‍🏫 PANDUAN PENDIDIK</div><h2>Kelola pembelajaran dengan praktis</h2><p>Ruang guru menyediakan perangkat ajar, pratinjau materi, bank soal, dan rubrik penilaian.</p></div>", unsafe_allow_html=True)
    st.markdown("""### Alur penggunaan
1. Pilih **Guru** pada bagian *Pilih Ruang Akses* di sidebar.
2. Buka **Perangkat Ajar** untuk meninjau CP, ATP, tujuan pembelajaran, dan materi.
3. Buka **Bank Soal & Evaluasi** untuk memeriksa pertanyaan, opsi, kunci, serta pembahasan.
4. Buka **Rubrik & Penilaian** untuk meninjau kriteria proyek dan menentukan ambang ketercapaian sementara.
5. Pilih kembali **Siswa** untuk melihat tampilan yang digunakan peserta didik.

### 🔎 Catatan penting
- Pilihan Guru/Siswa saat ini adalah pemisahan antarmuka, bukan autentikasi akun.
- Jangan menaruh data pribadi atau nilai rahasia siswa di aplikasi sebelum sistem login dan penyimpanan aman disiapkan.
- Pengaturan ambang nilai berlaku sementara selama sesi dan belum tersimpan permanen.
- Pastikan CP, ATP, dan instrumen evaluasi sesuai dokumen final yang disetujui dosen/guru pembimbing.""")

elif page == "Beranda":
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🎙️ DIGITAL NEWSROOM · BAHASA INDONESIA</div><h2>👋 Halo, Jurnalis Muda!</h2><p>Selamat datang di <b>AI Tutor Teks Berita</b>. Yuk, belajar menemukan fakta, mengurai unsur 5W+1H, memeriksa kebenaran informasi, dan menyusun berita yang menarik sekaligus bertanggung jawab.</p><div style='margin-top:15px'><span class='mini-tag'>🧭 Berpikir Kritis</span><span class='mini-tag'>🔎 Cek Fakta</span><span class='mini-tag'>✍️ Menulis Kreatif</span></div></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("📚 Materi inti", "10 topik", "Belajar bertahap")
    c2.metric("📝 Evaluasi", "10 soal", "Nilai otomatis")
    c3.metric("🔎 Fokus utama", "5W+1H", "Unsur berita")
    st.markdown("<div class='section-label'>🚀 JELAJAHI FITUR PEMBELAJARAN</div>", unsafe_allow_html=True)
    cards = st.columns(5)
    features = [("🏠","Beranda","CP, ATP, tujuan belajar","#eaf3ff"),("📖","Petunjuk Penggunaan","Panduan penggunaan aplikasi","#f2eaff"),("🗞️","Materi","Konsep, struktur, 5W+1H, fakta dan opini","#e5fbf3"),("📝","Evaluasi","Latihan pilihan ganda dan pembahasan","#fff4dc"),("🏆","Rubrik Penilaian","Kriteria skor dan proyek berita","#ffe9e9")]
    for col,(emoji,title,desc,bg) in zip(cards,features):
        with col:
            st.markdown(f"<div class='feature-card' style='background:linear-gradient(160deg,{bg},#ffffff)'><div class='emoji'>{emoji}</div><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
    left,right = st.columns([1.35,1])
    with left:
        st.markdown("<div class='section-label'>🎯 TUJUAN PEMBELAJARAN</div>", unsafe_allow_html=True)
        for item in TUJUAN: st.markdown(f"✅ {item}")
    with right:
        st.markdown("<div class='section-label'>📌 KUNCI JADI JURNALIS MUDA</div>", unsafe_allow_html=True)
        st.markdown("<div class='quote-card'>📰 “Berita yang baik bukan sekadar cepat dibaca, tetapi juga akurat, berimbang, dan bisa dipertanggungjawabkan.”<br><br><b>— Prinsip belajar kita</b></div>", unsafe_allow_html=True)
    with st.expander("📋 Lihat Capaian Pembelajaran (CP)"):
        st.info(CP)
    with st.expander("🛤️ Lihat Alur Tujuan Pembelajaran (ATP)"):
        for item in ATP: st.markdown(f"- {item}")
    st.success("✨ Mulai dari Petunjuk Penggunaan, lanjutkan ke Materi, lalu uji pemahamanmu melalui Evaluasi!")

elif page == "Petunjuk Penggunaan":
    st.title("📖 Petunjuk Penggunaan")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🧭 PANDUAN NAVIGASI</div><h2>Kenali ruang belajarmu!</h2><p>Ikuti alur berikut agar pengalaman belajar teks berita lebih terarah dan maksimal.</p></div>", unsafe_allow_html=True)
    st.markdown("""### Urutan belajar yang disarankan
1. Buka **Beranda** untuk membaca CP, ATP, dan tujuan pembelajaran.
2. Buka **Materi** dan pelajari topik secara berurutan.
3. Baca contoh teks berita dan periksa analisis unsur 5W+1H.
4. Gunakan bagian **Tanya AI Tutor** pada halaman Materi untuk mencari penjelasan tambahan.
5. Buka **Evaluasi**, pilih satu jawaban untuk setiap soal, lalu tekan **Kirim Evaluasi**.
6. Buka **Rubrik Penilaian** untuk memahami skor dan kategori hasil.

### Tips menggunakan AI Tutor
- Ajukan pertanyaan yang jelas dan spesifik, misalnya “Apa perbedaan fakta dan opini dalam berita?”
- Jawaban AI Tutor bergantung pada materi yang tersedia di folder `database`.
- Jika jawaban tidak ditemukan, coba gunakan kata kunci lain atau periksa materi secara langsung.
- Periksa kembali informasi penting. Jangan menganggap semua informasi di internet benar tanpa verifikasi.

### Catatan
Evaluasi otomatis memeriksa pilihan ganda berdasarkan kunci jawaban yang disediakan. Nilai latihan ini merupakan umpan balik belajar dan dapat disesuaikan dengan kebijakan guru.""")

elif page == "Materi":
    st.title("🗞️ Materi Pembelajaran Teks Berita")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🔎 NEWS KNOWLEDGE CENTER</div><h2>Bekali diri dengan fakta!</h2><p>Pilih bagian materi untuk membuka penjelasan. Gunakan Tanya AI Tutor jika membutuhkan bantuan tambahan.</p></div>", unsafe_allow_html=True)
    st.write("Pelajari konsep, struktur, unsur, dan cara memeriksa keakuratan berita sebelum mulai menulis.")
    with st.expander("Capaian Pembelajaran dan Tujuan", expanded=True):
        st.markdown("**Capaian Pembelajaran**")
        st.write(CP)
        st.markdown("**Tujuan Pembelajaran**")
        for i,item in enumerate(TUJUAN,1): st.markdown(f"{i}. {item}")
    for title, body in MATERI.items():
        with st.expander(title, expanded=False):
            st.markdown(body)
    st.divider()
    st.subheader("🧠 Tanya AI Tutor")
    st.write("AI Tutor mencari jawaban dari file materi `.txt` yang tersimpan di folder `database`.")
    docs = load_database()
    if not docs:
        st.warning("Folder `database` belum ditemukan atau belum berisi file TXT. Materi pembelajaran di atas tetap dapat digunakan, tetapi pencarian AI Tutor membutuhkan file TXT.")
    for item in st.session_state.chat:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])
            if item.get("source"):
                st.caption(f"📚 Sumber: {item['source']}")
    prompt = st.chat_input("Tanyakan sesuatu tentang Bahasa dan Sastra Indonesia...")
    if prompt:
        st.session_state.chat.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        answer, source = retrieve_answer(prompt, docs)
        if answer:
            with st.chat_message("assistant"):
                st.markdown(answer)
                st.caption(f"📚 Sumber: {source}")
            st.session_state.chat.append({"role":"assistant","content":answer,"source":source})
        else:
            message = "Maaf, materi yang sesuai belum ditemukan dalam database. Coba gunakan kata kunci yang lebih spesifik atau baca bagian materi di atas."
            with st.chat_message("assistant"): st.markdown(message)
            st.session_state.chat.append({"role":"assistant","content":message})

elif page == "Evaluasi":
    st.title("📝 Evaluasi Pemahaman Teks Berita")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>🎯 TEST YOUR NEWS IQ</div><h2>Siap menguji pemahaman?</h2><p>Jawab setiap soal dengan cermat. Ingat prinsip 5W+1H, objektivitas, struktur, dan verifikasi fakta.</p></div>", unsafe_allow_html=True)
    st.write("Pilih satu jawaban yang paling tepat untuk setiap soal. Terdapat 10 soal; setiap jawaban benar bernilai 10.")
    with st.form("quiz_form"):
        selected = {}
        for i, q in enumerate(SOAL):
            st.markdown(f"**{i+1}. {q['q']}**")
            selected[i] = st.radio("Pilih jawaban:", q["opts"], index=None, key=f"q_{i}", label_visibility="collapsed")
            st.divider()
        submitted = st.form_submit_button("Kirim Evaluasi", type="primary")
    if submitted:
        st.session_state.answers = selected
        st.session_state.submitted = True
    if st.session_state.submitted:
        correct = sum(1 for i,q in enumerate(SOAL) if st.session_state.answers.get(i) == q["opts"][q["key"]])
        score = correct * 10
        st.subheader("Hasil Evaluasi")
        a,b = st.columns(2)
        a.metric("Jawaban benar", f"{correct} dari {len(SOAL)}")
        b.metric("Nilai", score)
        if score >= 90: st.success("Sangat Baik — pemahaman materi sudah sangat kuat.")
        elif score >= 80: st.success("Baik — sebagian besar konsep sudah dipahami.")
        elif score >= 70: st.info("Cukup — pelajari kembali beberapa bagian materi.")
        elif score >= 60: st.warning("Kurang — perlu penguatan pada konsep penting.")
        else: st.error("Perlu Bimbingan — pelajari kembali materi dan coba lagi.")
        st.subheader("Pembahasan Jawaban")
        for i,q in enumerate(SOAL):
            user_answer = st.session_state.answers.get(i)
            is_correct = user_answer == q["opts"][q["key"]]
            st.markdown(f"**Soal {i+1}: {'Benar' if is_correct else 'Belum tepat'}**")
            st.write(f"Jawaban benar: {q['opts'][q['key']]}")
            st.caption(q["why"])
        if st.button("Ulangi Evaluasi"):
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.rerun()

elif page == "Rubrik Penilaian":
    st.title("🏆 Rubrik Penilaian")
    st.markdown("<div class='hero-news'><div class='hero-kicker'>📊 TRANSPARANSI PENILAIAN</div><h2>Kenali kriteria keberhasilanmu</h2><p>Gunakan rubrik berikut untuk memahami penilaian evaluasi dan kualitas proyek menulis teks berita.</p></div>", unsafe_allow_html=True)
    st.subheader("A. Penilaian pilihan ganda")
    st.markdown("Setiap soal memiliki bobot yang sama. Jawaban benar memperoleh 10 poin, sedangkan jawaban salah atau tidak dijawab memperoleh 0 poin. Skor maksimal adalah 100.")
    st.latex(r"\text{Nilai akhir} = \frac{\text{jumlah jawaban benar}}{10} \times 100")
    st.subheader("B. Interpretasi nilai")
    st.table({"Rentang Nilai":["90–100","80–89","70–79","60–69","0–59"],"Kategori":["Sangat Baik","Baik","Cukup","Kurang","Sangat Kurang"],"Interpretasi":["Menguasai materi dengan sangat baik.","Memahami sebagian besar konsep.","Memahami dasar materi tetapi perlu penguatan.","Belum memahami beberapa konsep penting.","Memerlukan bimbingan dan pembelajaran remedial."]})
    st.caption("Rentang kategori dapat disesuaikan dengan Kriteria Ketercapaian Tujuan Pembelajaran (KKTP) yang digunakan guru.")
    st.subheader("C. Rubrik proyek menulis teks berita")
    st.write("Rubrik berikut dapat digunakan guru sebagai panduan saat menilai proyek teks berita; penilaian proyek tidak dihitung otomatis oleh aplikasi.")
    st.table({"Aspek":["Kelengkapan 5W+1H","Struktur berita","Fakta dan akurasi sumber","Objektivitas dan bahasa","Ejaan dan penyajian"],"4 — Sangat Baik":["Unsur lengkap dan jelas","Judul, teras, tubuh, ekor tersusun efektif","Fakta kuat dan sumber dapat diperiksa","Netral, lugas, tidak menyesatkan","Hampir tanpa kesalahan; penyajian sangat jelas"],"3 — Baik":["Sebagian besar unsur lengkap","Struktur jelas dengan kekurangan kecil","Sebagian besar informasi didukung sumber","Cukup objektif dan jelas","Ada sedikit kesalahan"],"2 — Cukup":["Beberapa unsur penting hilang","Struktur kurang seimbang","Sebagian klaim belum didukung","Masih ada opini atau kata berlebihan","Kesalahan cukup mengganggu"],"1 — Perlu Bimbingan":["Banyak unsur tidak tersedia","Struktur sulit dikenali","Sumber tidak jelas atau informasi meragukan","Bahasa subjektif/menyesatkan","Banyak kesalahan yang mengganggu pemahaman"]})
    st.markdown("**Saran penghitungan nilai proyek:** jumlahkan skor yang diperoleh, bagi dengan skor maksimal, lalu kalikan 100. Jika menggunakan lima aspek dengan skor maksimal 4, skor maksimalnya 20.")
    st.latex(r"\text{Nilai proyek} = \frac{\text{skor diperoleh}}{20} \times 100")
    st.subheader("D. Kriteria proses belajar")
    st.markdown("Guru juga dapat mengamati kemandirian, kemampuan mengajukan pertanyaan, penggunaan alasan yang logis, keterbukaan terhadap masukan, dan kreativitas saat menyusun serta mempresentasikan berita.")

st.sidebar.divider()
st.sidebar.markdown("<div style='text-align:center;padding:8px;font-size:11px;opacity:.85'>📰 AI TUTOR<br>Literasi · Akurasi · Kreativitas</div>", unsafe_allow_html=True)
