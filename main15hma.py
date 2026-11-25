import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
import time
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ML Analytics Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS: ORANGE & WHITE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1E293B;
    }

    .stApp {
        background-color: #FFFFFF;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFF7ED;
        border-right: 1px solid #FFEDD5;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .office-hero {
        background: #FFFFFF;
        border-left: 6px solid #F97316;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(249, 115, 22, 0.08);
    }
    .office-badge {
        display: inline-block;
        background-color: #FFEDD5;
        color: #EA580C;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .office-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.25rem;
    }
    .office-subtitle {
        font-size: 0.95rem;
        color: #64748B;
    }
    .office-subtitle a {
        color: #EA580C;
        text-decoration: none;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #F97316;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
        color: #FFFFFF;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.2rem;
        width: 100%;
        transition: all 0.25s ease;
        box-shadow: 0 4px 10px rgba(234, 88, 12, 0.25);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(234, 88, 12, 0.35);
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        padding-bottom: 8px;
        border-bottom: 2px solid #FFEDD5;
        margin-bottom: 1rem;
    }

    .param-card {
        background-color: #FFFBF7;
        border: 1px solid #FED7AA;
        border-left: 4px solid #F97316;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        font-size: 0.9rem;
        line-height: 1.45;
    }
    .param-title {
        font-weight: 700;
        color: #C2410C;
        margin-bottom: 3px;
    }
    .param-val {
        display: inline-block;
        background-color: #FFEDD5;
        color: #9A3412;
        font-weight: 700;
        padding: 1px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
        margin-left: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CHIBI + SPEECH BUBBLE RENDERER ---
def render_chibi(role: str = "analyst", message: str = "Halo! Siap menganalisis data hari ini?", mood: str = "neutral", height: int = 135):
    mood_styles = {
        "neutral": {"bg": "#FFF7ED", "border": "#F97316", "text": "#9A3412"},
        "success": {"bg": "#ECFDF5", "border": "#10B981", "text": "#065F46"},
        "warning": {"bg": "#FEF2F2", "border": "#EF4444", "text": "#991B1B"}
    }
    style = mood_styles.get(mood, mood_styles["neutral"])

    if role == "analyst":
        svg_char = """
        <svg viewBox="0 0 140 140" width="110" height="110">
            <ellipse cx="70" cy="128" rx="32" ry="6" fill="#FED7AA" class="shadow-anim"/>
            <g class="chibi-float">
                <path d="M45 92 Q70 85 95 92 L102 122 L38 122 Z" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
                <polygon points="70,92 65,105 70,118 75,105" fill="#F97316"/>
                <circle cx="70" cy="56" r="32" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2"/>
                <path d="M38 52 C38 22, 102 22, 102 52 C95 36, 80 35, 70 42 C60 35, 45 36, 38 52 Z" fill="#1E293B"/>
                <rect x="48" y="50" width="17" height="12" rx="3" fill="none" stroke="#EA580C" stroke-width="2.2"/>
                <rect x="75" y="50" width="17" height="12" rx="3" fill="none" stroke="#EA580C" stroke-width="2.2"/>
                <line x1="65" y1="56" x2="75" y2="56" stroke="#EA580C" stroke-width="2.2"/>
                <circle cx="56.5" cy="56" r="2.8" fill="#0F172A" class="eye-blink"/>
                <circle cx="83.5" cy="56" r="2.8" fill="#0F172A" class="eye-blink"/>
                <ellipse cx="48" cy="65" rx="4" ry="2" fill="#FB923C" opacity="0.5"/>
                <ellipse cx="92" cy="65" rx="4" ry="2" fill="#FB923C" opacity="0.5"/>
                <path d="M64 67 Q70 73 76 67" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round"/>
                <circle cx="106" cy="96" r="8" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" class="hand-wave"/>
            </g>
        </svg>
        """
    elif role == "botanist":
        svg_char = """
        <svg viewBox="0 0 140 140" width="105" height="105">
            <ellipse cx="70" cy="128" rx="30" ry="5" fill="#FED7AA" class="shadow-anim"/>
            <g class="chibi-float">
                <path d="M46 92 Q70 86 94 92 L100 122 L40 122 Z" fill="#F97316"/>
                <circle cx="70" cy="56" r="31" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2"/>
                <path d="M39 50 C40 20, 100 20, 101 50 C90 34, 50 34, 39 50 Z" fill="#334155"/>
                <circle cx="57" cy="57" r="3" fill="#0F172A" class="eye-blink"/>
                <circle cx="83" cy="57" r="3" fill="#0F172A" class="eye-blink"/>
                <path d="M65 67 Q70 72 75 67" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round"/>
                <g transform="translate(92, 28)">
                    <circle cx="0" cy="-6" r="5" fill="#F97316"/>
                    <circle cx="6" cy="0" r="5" fill="#FB923C"/>
                    <circle cx="0" cy="6" r="5" fill="#F97316"/>
                    <circle cx="-6" cy="0" r="5" fill="#FB923C"/>
                    <circle cx="0" cy="0" r="4" fill="#FEF08A"/>
                </g>
            </g>
        </svg>
        """
    else:
        svg_char = """
        <svg viewBox="0 0 140 140" width="105" height="105">
            <ellipse cx="70" cy="128" rx="30" ry="5" fill="#FED7AA" class="shadow-anim"/>
            <g class="chibi-float">
                <path d="M45 92 Q70 85 95 92 L102 122 L38 122 Z" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>
                <path d="M58 92 L58 110 M82 92 L82 110" stroke="#F97316" stroke-width="2.5"/>
                <circle cx="70" cy="56" r="31" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2"/>
                <path d="M39 52 C39 22, 101 22, 101 52 C88 36, 52 36, 39 52 Z" fill="#1E293B"/>
                <circle cx="70" cy="31" r="7" fill="#E2E8F0" stroke="#F97316" stroke-width="2"/>
                <circle cx="57" cy="57" r="3" fill="#0F172A" class="eye-blink"/>
                <circle cx="83" cy="57" r="3" fill="#0F172A" class="eye-blink"/>
                <path d="M65 67 Q70 72 75 67" fill="none" stroke="#0F172A" stroke-width="2" stroke-linecap="round"/>
                <path d="M105 42 C105 37, 98 37, 98 42 C98 37, 91 37, 91 42 C91 48, 98 53, 98 53 C98 53, 105 48, 105 42 Z" fill="#EA580C" class="heart-pulse"/>
            </g>
        </svg>
        """

    html_code = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&display=swap');
        .chibi-wrapper {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 12px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 4px;
        }}
        .speech-bubble {{
            position: relative;
            background: {style['bg']};
            border: 2px solid {style['border']};
            color: {style['text']};
            border-radius: 14px;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 230px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .speech-bubble::after {{
            content: '';
            position: absolute;
            right: -10px;
            top: 50%;
            transform: translateY(-50%);
            border-width: 8px 0 8px 10px;
            border-style: solid;
            border-color: transparent transparent transparent {style['border']};
        }}
        .speech-bubble::before {{
            content: '';
            position: absolute;
            right: -7px;
            top: 50%;
            transform: translateY(-50%);
            border-width: 6px 0 6px 8px;
            border-style: solid;
            border-color: transparent transparent transparent {style['bg']};
            z-index: 1;
        }}
        .chibi-float {{ animation: floatAnim 2.8s ease-in-out infinite; transform-origin: center; }}
        .shadow-anim {{ animation: shadowScale 2.8s ease-in-out infinite; transform-origin: center; }}
        .eye-blink {{ animation: blinkAnim 4s infinite; transform-origin: center; }}
        .hand-wave {{ animation: waveAnim 1.5s ease-in-out infinite; transform-origin: 95px 96px; }}
        .heart-pulse {{ animation: pulseAnim 1.2s ease-in-out infinite; transform-origin: 98px 45px; }}
        @keyframes popIn {{
            0% {{ opacity: 0; transform: scale(0.85) translateX(10px); }}
            100% {{ opacity: 1; transform: scale(1) translateX(0); }}
        }}
        @keyframes floatAnim {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-5px); }} }}
        @keyframes shadowScale {{ 0%, 100% {{ transform: scale(1); opacity: 0.7; }} 50% {{ transform: scale(0.85); opacity: 0.4; }} }}
        @keyframes blinkAnim {{ 0%, 92%, 100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(0.1); }} }}
        @keyframes waveAnim {{ 0%, 100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(-18deg); }} }}
        @keyframes pulseAnim {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.25); }} }}
    </style>
    <div class="chibi-wrapper">
        <div class="speech-bubble">{message}</div>
        <div>{svg_char}</div>
    </div>
    """
    components.html(html_code, height=height)

# --- 4. CACHE MODEL LOADER & STATE RESETTER ---
@st.cache_resource
def load_model(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

def reset_prediction_states():
    """Menghapus jejak prediksi lama saat pengguna berpindah modul atau mengubah mode input."""
    for key in ["last_iris_sig", "last_heart_sig", "iris_chibi_msg", "iris_chibi_mood", "heart_chibi_msg", "heart_chibi_mood"]:
        st.session_state.pop(key, None)

# --- 5. CORPORATE HEADER ---
col_head1, col_head2 = st.columns([3.2, 2.3])
with col_head1:
    st.markdown("""
    <div class="office-hero">
        <div class="office-badge">Enterprise Analytics Suite</div>
        <div class="office-title">Machine Learning Predictive Portal</div>
        <div class="office-subtitle">
            Automated Classification & Decision Support System • Created by 
            <a href="https://www.linkedin.com/in/hanna-mutia-agista/" target="_blank">@hanna.agista</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    render_chibi(
        role="analyst",
        message="Halo! Pilih modul di sidebar kiri untuk mulai prediksi data ya! 👋",
        mood="neutral",
        height=145
    )

# --- 6. SIDEBAR NAVIGATION (HEART DISEASE DEFAULT) ---
st.sidebar.markdown("### 🗂️ Workspace Module")
app_mode = st.sidebar.selectbox(
    "Pilih Layanan Prediksi:",
    ("❤️ Heart Disease Assessment", "🌸 Iris Species Classification"),
    on_change=reset_prediction_states
)
st.sidebar.markdown("---")

# ==========================================
# MODULE 1: HEART DISEASE ASSESSMENT
# ==========================================
def heart_page():
    DEFAULT_MSG = "Masukkan parameter klinis pasien untuk cek risiko jantung! 🩺"
    DEFAULT_MOOD = "neutral"

    st.sidebar.markdown("#### ⚙️ Parameter Klinis Pasien")
    input_method = st.sidebar.radio(
        "Sumber Data:",
        ["Manual Input", "Upload CSV"],
        horizontal=True,
        key="heart_radio",
        on_change=reset_prediction_states
    )

    if input_method == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type=["csv"], key="heart_csv")
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
        else:
            reset_prediction_states()
            c_title, c_chibi = st.columns([3.2, 2.3])
            with c_title:
                st.subheader("❤️ Heart Disease Risk Assessment")
                st.caption("Evaluasi klinis berbasis Machine Learning untuk deteksi dini risiko penyakit kardiovaskular.")
            with c_chibi:
                render_chibi(role="doctor", message="Silakan unggah file CSV data klinis pasien di sidebar kiri! 📂", mood="neutral", height=120)
            st.info("👈 Silakan unggah file CSV pada panel navigasi di sebelah kiri.")
            return
    else:
        cp = st.sidebar.slider('Chest pain type (cp)', 1, 4, 2)
        thalach = st.sidebar.slider("Max heart rate (thalach)", 71, 202, 150)
        slope = st.sidebar.slider("Kemiringan segmen ST (slope)", 0, 2, 1)
        oldpeak = st.sidebar.slider("Depresi ST (oldpeak)", 0.00, 6.20, 1.00, step=0.01, format="%.2f")
        exang = st.sidebar.selectbox("Exercise induced angina (exang)", [0, 1], format_func=lambda x: "Ya (1)" if x == 1 else "Tidak (0)")
        ca = st.sidebar.slider("Number of major vessels (ca)", 0, 3, 0)
        thal = st.sidebar.slider("Hasil tes thalium (thal)", 1, 3, 2)
        sex_label = st.sidebar.selectbox("Jenis Kelamin", ('Perempuan', 'Pria'))
        sex = 0 if sex_label == "Perempuan" else 1
        age = st.sidebar.slider("Usia (Tahun)", 29, 77, 45)
        
        input_df = pd.DataFrame({
            'cp': [cp], 'thalach': [thalach], 'slope': [slope],
            'oldpeak': [round(oldpeak, 2)], 'exang': [exang], 'ca': [ca],
            'thal': [thal], 'sex': [sex], 'age': [age]
        })

    predict_btn = st.sidebar.button("Jalankan Evaluasi Risiko", key="btn_heart")

    prediction_done = False
    if predict_btn:
        loaded_model = load_model("generate_heart_disease.pkl")
        predictions = loaded_model.predict(input_df)
        results = ['No Heart Disease' if p == 0 else 'Yes Heart Disease' for p in predictions]
        prediction_done = True
        st.session_state.last_heart_sig = input_df.to_json()

        if len(results) == 1:
            if predictions[0] == 1:
                st.session_state.heart_chibi_msg = "Perhatian! Terdeteksi <b>indikasi risiko jantung</b>. Segera konsultasi medis! ⚠️"
                st.session_state.heart_chibi_mood = "warning"
            else:
                st.session_state.heart_chibi_msg = "Kabar baik! Hasil analisis menunjukkan <b>risiko jantung rendah</b>. 💚"
                st.session_state.heart_chibi_mood = "success"
        else:
            st.session_state.heart_chibi_msg = f"Evaluasi batch selesai untuk <b>{len(results):,} pasien</b>! 📋"
            st.session_state.heart_chibi_mood = "neutral"
    else:
        st.session_state.pop("last_heart_sig", None)
        st.session_state.heart_chibi_msg = DEFAULT_MSG
        st.session_state.heart_chibi_mood = DEFAULT_MOOD

    c_title, c_chibi = st.columns([3.2, 2.3])
    with c_title:
        st.subheader("❤️ Heart Disease Risk Assessment")
        st.caption("Evaluasi klinis berbasis Machine Learning untuk deteksi dini risiko penyakit kardiovaskular.")
    with c_chibi:
        render_chibi(
            role="doctor",
            message=st.session_state.heart_chibi_msg,
            mood=st.session_state.heart_chibi_mood,
            height=120
        )

    col_left, col_right = st.columns([1.25, 1.75], gap="large")

    with col_left:
        st.markdown('<div class="section-header">📖 Keterangan & Arti Parameter Klinis</div>', unsafe_allow_html=True)
        
        if len(input_df) == 1:
            row = input_df.iloc[0]
            cp_map = {
                1: "Typical Angina (nyeri dada khas akibat penyempitan pembuluh darah jantung)",
                2: "Atypical Angina (nyeri dada tidak khas yang dicurigai terkait jantung)",
                3: "Non-Anginal Pain (nyeri dada yang umumnya bukan berasal dari jantung)",
                4: "Asymptomatic (tidak merasakan gejala nyeri dada)"
            }
            slope_map = {
                0: "Upsloping (kemiringan segmen ST menanjak saat puncak latihan)",
                1: "Flat (kemiringan segmen ST mendatar — sering dikaitkan dengan iskemia)",
                2: "Downsloping (kemiringan segmen ST menurun — indikasi gangguan aliran darah)"
            }
            thal_map = {
                1: "Normal (aliran darah ke otot jantung normal)",
                2: "Fixed Defect (kerusakan jaringan jantung permanen / bekas serangan jantung)",
                3: "Reversible Defect (gangguan aliran darah sementara saat jantung bekerja keras)"
            }

            clinical_items = [
                ("age & sex (Usia & Jenis Kelamin)", f"{int(row['age'])} Thn • {'Pria' if int(row['sex']) == 1 else 'Perempuan'}",
                 "Faktor demografis dasar pasien. Risiko penyakit kardiovaskular cenderung meningkat seiring bertambahnya usia."),
                ("cp — Chest Pain Type", f"Tipe {int(row['cp'])}",
                 f"Jenis nyeri dada yang dialami pasien: <b>{cp_map.get(int(row['cp']), '-')}</b>."),
                ("thalach — Max Heart Rate", f"{int(row['thalach'])} bpm",
                 "Detak jantung maksimum (denyut per menit) yang dicapai pasien selama tes beban/olahraga."),
                ("exang — Exercise Induced Angina", f"{'Ya (1)' if int(row['exang']) == 1 else 'Tidak (0)'}",
                 "Menunjukkan apakah aktivitas fisik/olahraga memicu munculnya nyeri dada (angina) akibat kurangnya suplai oksigen ke jantung."),
                ("oldpeak — ST Depression", f"{row['oldpeak']:.2f} mm",
                 "Besarnya penurunan segmen ST pada grafik EKG saat berolahraga dibandingkan saat istirahat. Nilai tinggi mengindikasikan stres/iskemia pada otot jantung."),
                ("slope — ST Segment Slope", f"Kode {int(row['slope'])}",
                 f"Pola kemiringan segmen ST pada puncak latihan EKG: <b>{slope_map.get(int(row['slope']), '-')}</b>."),
                ("ca — Major Vessels", f"{int(row['ca'])} pembuluh",
                 "Jumlah pembuluh darah koroner utama (0–3) yang terdeteksi mengalami penyempitan atau penyumbatan melalui pemeriksaan fluoroskopi."),
                ("thal — Thalassemia / Thallium Stress Test", f"Kode {int(row['thal'])}",
                 f"Hasil pemindaian aliran darah otot jantung menggunakan tes Thallium: <b>{thal_map.get(int(row['thal']), '-')}</b>.")
            ]

            for title, val, desc in clinical_items:
                st.markdown(f"""
                <div class="param-card">
                    <div class="param-title">{title} <span class="param-val">{val}</span></div>
                    <div style="color: #475569;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Mode batch CSV aktif: **{len(input_df):,} baris data pasien** siap dievaluasi.")
            with st.expander("Lihat Penjelasan Arti Setiap Kolom CSV", expanded=True):
                st.markdown("""
                * **`cp`**: Tipe nyeri dada (1 = *Typical Angina*, 2 = *Atypical Angina*, 3 = *Non-anginal*, 4 = *Asymptomatic*).
                * **`thalach`**: Detak jantung maksimum yang dicapai saat tes beban (bpm).
                * **`slope`**: Kemiringan segmen ST pada puncak latihan EKG (0 = *Upsloping*, 1 = *Flat*, 2 = *Downsloping*).
                * **`oldpeak`**: Tingkat depresi segmen ST akibat olahraga dibandingkan kondisi istirahat.
                * **`exang`**: Nyeri dada yang dipicu olahraga (1 = Ya, 0 = Tidak).
                * **`ca`**: Jumlah pembuluh darah utama (0–3) yang terdeteksi mengalami penyumbatan via fluoroskopi.
                * **`thal`**: Hasil tes aliran darah Thallium (1 = Normal, 2 = *Fixed Defect*, 3 = *Reversible Defect*).
                * **`sex`**: Jenis kelamin pasien (1 = Pria, 0 = Perempuan).
                * **`age`**: Usia pasien dalam tahun.
                """)

    with col_right:
        st.markdown('<div class="section-header">🩺 Hasil Diagnosa Model</div>', unsafe_allow_html=True)
        if prediction_done:
            bar = st.progress(0, text="Mengevaluasi indikator klinis...")
            for i in range(100):
                time.sleep(0.005)
                bar.progress(i + 1, text="Mengevaluasi indikator klinis...")
            bar.empty()

            if len(results) == 1:
                is_risk = predictions[0] == 1
                if is_risk:
                    st.error("⚠️ **Terdeteksi Risiko Penyakit Jantung (Yes Heart Disease)**")
                else:
                    st.success("✅ **Tidak Terdeteksi Risiko Penyakit Jantung (No Heart Disease)**")

                if hasattr(loaded_model, "predict_proba"):
                    risk_prob = loaded_model.predict_proba(input_df)[0][1] * 100
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=risk_prob,
                        number={'suffix': "%", 'valueformat': '.2f', 'font': {'color': '#0F172A'}},
                        title={'text': "Indeks Probabilitas Risiko", 'font': {'size': 16}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickformat': '.2f'},
                            'bar': {'color': "#EF4444" if risk_prob > 50 else "#10B981"},
                            'steps': [
                                {'range': [0, 40], 'color': "#FFF7ED"},
                                {'range': [40, 70], 'color': "#FFEDD5"},
                                {'range': [70, 100], 'color': "#FED7AA"}
                            ],
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=280,
                        margin=dict(t=40, b=10, l=20, r=20)
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                output_df = input_df.copy()
                output_df['Prediction'] = results
                st.dataframe(output_df.style.format("{:.2f}", subset=input_df.select_dtypes(include="float").columns), use_container_width=True, hide_index=True)
        else:
            st.info("Lengkapi data klinis di sidebar, lalu klik tombol **Jalankan Evaluasi Risiko**.")

# ==========================================
# MODULE 2: IRIS SPECIES CLASSIFICATION
# ==========================================
def iris_page():
    DEFAULT_MSG = "Atur ukuran kelopak di kiri, lalu klik tombol prediksi! 🌸"
    DEFAULT_MOOD = "neutral"

    st.sidebar.markdown("#### ⚙️ Konfigurasi Input")
    input_method = st.sidebar.radio(
        "Sumber Data:",
        ["Manual Input", "Upload CSV"],
        horizontal=True,
        key="iris_radio",
        on_change=reset_prediction_states
    )

    if input_method == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type=["csv"], key="iris_csv")
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
        else:
            reset_prediction_states()
            c_title, c_chibi = st.columns([3.2, 2.3])
            with c_title:
                st.subheader("🌸 Iris Species Classification")
                st.caption("Klasifikasi otomatis spesies bunga Iris (Setosa, Versicolor, Virginica) berdasarkan parameter morfologi UCIML.")
            with c_chibi:
                render_chibi(role="botanist", message="Silakan unggah file CSV bunga Iris di sidebar kiri ya! 📂", mood="neutral", height=120)
            st.info("👈 Silakan unggah file CSV pada panel navigasi di sebelah kiri.")
            return
    else:
        SepalLengthCm = st.sidebar.slider('Sepal Length (cm)', 4.30, 10.00, 6.50, step=0.01, format="%.2f")
        SepalWidthCm = st.sidebar.slider('Sepal Width (cm)', 2.00, 5.00, 3.30, step=0.01, format="%.2f")
        PetalLengthCm = st.sidebar.slider('Petal Length (cm)', 1.00, 9.00, 4.00, step=0.01, format="%.2f")
        PetalWidthCm = st.sidebar.slider('Petal Width (cm)', 0.10, 5.00, 1.40, step=0.01, format="%.2f")
        
        input_df = pd.DataFrame({
            'SepalLengthCm': [round(SepalLengthCm, 2)],
            'SepalWidthCm': [round(SepalWidthCm, 2)],
            'PetalLengthCm': [round(PetalLengthCm, 2)],
            'PetalWidthCm': [round(PetalWidthCm, 2)]
        })

    current_sig = input_df.to_json()
    if st.session_state.get("last_iris_sig") != current_sig:
        st.session_state.iris_chibi_msg = DEFAULT_MSG
        st.session_state.iris_chibi_mood = DEFAULT_MOOD

    predict_btn = st.sidebar.button("Jalankan Analisis Prediksi", key="btn_iris")

    prediction_done = False
    if predict_btn:
        loaded_model = load_model("model_iris.pkl")
        predictions = loaded_model.predict(input_df)
        label_map = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}
        results = [label_map.get(p, str(p)) for p in predictions]
        prediction_done = True
        st.session_state.last_iris_sig = current_sig

        if len(results) == 1:
            st.session_state.iris_chibi_msg = f"Ketemu! Bunga ini adalah spesies <b>{results[0]}</b>! ✨"
            st.session_state.iris_chibi_mood = "success"
        else:
            st.session_state.iris_chibi_msg = f"Selesai! Total <b>{len(results):,} data</b> berhasil diklasifikasikan! 📊"
            st.session_state.iris_chibi_mood = "success"
    else:
        st.session_state.pop("last_iris_sig", None)
        st.session_state.iris_chibi_msg = DEFAULT_MSG
        st.session_state.iris_chibi_mood = DEFAULT_MOOD

    c_title, c_chibi = st.columns([3.2, 2.3])
    with c_title:
        st.subheader("🌸 Iris Species Classification")
        st.caption("Klasifikasi otomatis spesies bunga Iris (Setosa, Versicolor, Virginica) berdasarkan parameter morfologi UCIML.")
    with c_chibi:
        render_chibi(
            role="botanist",
            message=st.session_state.iris_chibi_msg,
            mood=st.session_state.iris_chibi_mood,
            height=120
        )

    col_left, col_right = st.columns([1.25, 1.75], gap="large")

    with col_left:
        st.markdown('<div class="section-header">📖 Keterangan & Arti Parameter Morfologi</div>', unsafe_allow_html=True)
        
        if len(input_df) == 1:
            row = input_df.iloc[0]
            iris_items = [
                ("SepalLengthCm — Panjang Kelopak Luar", f"{row['SepalLengthCm']:.2f} cm",
                 "Panjang daun kelopak luar bunga (<i>sepal</i>) yang berfungsi melindungi kuncup sebelum mekar. Umumnya berkisar antara 4.30 – 7.90 cm."),
                ("SepalWidthCm — Lebar Kelopak Luar", f"{row['SepalWidthCm']:.2f} cm",
                 "Lebar bagian terluas dari kelopak luar bunga. <i>Iris-setosa</i> cenderung memiliki sepal yang lebih lebar dibandingkan dua spesies lainnya."),
                ("PetalLengthCm — Panjang Mahkota Bunga", f"{row['PetalLengthCm']:.2f} cm",
                 "Panjang daun mahkota bagian dalam (<i>petal</i>) yang berwarna cerah. Merupakan pembeda paling kuat: <i>Setosa</i> pendek (&lt; 2.00 cm), <i>Versicolor</i> sedang (3.00–5.00 cm), dan <i>Virginica</i> panjang (&gt; 5.00 cm)."),
                ("PetalWidthCm — Lebar Mahkota Bunga", f"{row['PetalWidthCm']:.2f} cm",
                 "Lebar daun mahkota bagian dalam. Sangat berkorelasi dengan panjang petal dalam membedakan tingkat kematangan dan spesies bunga Iris.")
            ]

            for title, val, desc in iris_items:
                st.markdown(f"""
                <div class="param-card">
                    <div class="param-title">{title} <span class="param-val">{val}</span></div>
                    <div style="color: #475569;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Mode batch CSV aktif: **{len(input_df):,} baris data bunga** siap diklasifikasikan.")
            with st.expander("Lihat Penjelasan Arti Setiap Kolom CSV", expanded=True):
                st.markdown("""
                * **`SepalLengthCm`**: Panjang kelopak luar bunga (*sepal*) dalam satuan sentimeter.
                * **`SepalWidthCm`**: Lebar kelopak luar bunga (*sepal*) dalam satuan sentimeter.
                * **`PetalLengthCm`**: Panjang mahkota dalam bunga (*petal*) dalam satuan sentimeter.
                * **`PetalWidthCm`**: Lebar mahkota dalam bunga (*petal*) dalam satuan sentimeter.
                """)

    with col_right:
        st.markdown('<div class="section-header">📊 Hasil Evaluasi Model</div>', unsafe_allow_html=True)
        
        if len(input_df) == 1:
            fig_feat = px.bar(
                x=input_df.columns,
                y=input_df.iloc[0].values,
                labels={'x': 'Variabel Morfologi', 'y': 'Ukuran (cm)'},
                title="Profil Dimensi Input Aktif (cm)",
                color_discrete_sequence=['#F97316']
            )
            fig_feat.update_traces(
                texttemplate='%{y:.2f}',
                textposition='outside',
                hovertemplate='%{x}: <b>%{y:.2f} cm</b><extra></extra>'
            )
            fig_feat.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(tickformat='.2f', range=[0, max(input_df.iloc[0].values) * 1.2]),
                height=250,
                margin=dict(t=40, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_feat, use_container_width=True)

        if prediction_done:
            bar = st.progress(0, text="Memproses algoritma klasifikasi...")
            for i in range(100):
                time.sleep(0.005)
                bar.progress(i + 1, text="Memproses algoritma klasifikasi...")
            bar.empty()

            if len(results) == 1:
                st.toast("Analisis selesai!", icon="📊")
                st.metric(label="Hasil Klasifikasi Spesies", value=results[0], delta="Verified by Model")
                
                if hasattr(loaded_model, "predict_proba"):
                    probs = loaded_model.predict_proba(input_df)[0] * 100
                    prob_df = pd.DataFrame({
                        'Spesies': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'],
                        'Probabilitas (%)': probs
                    })
                    fig_prob = px.bar(
                        prob_df, x='Probabilitas (%)', y='Spesies', orientation='h',
                        title="Confidence Score per Kelas (%)",
                        text_auto='.2f',
                        color='Probabilitas (%)',
                        color_continuous_scale=['#FED7AA', '#F97316', '#C2410C']
                    )
                    fig_prob.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        coloraxis_showscale=False,
                        height=240,
                        xaxis=dict(range=[0, 112], tickformat='.2f')
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)
            else:
                output_df = input_df.copy()
                output_df['Prediction'] = results
                st.success(f"Selesai memproses {len(results):,} baris data.")
                st.dataframe(output_df.style.format("{:.2f}", subset=input_df.select_dtypes(include="float").columns), use_container_width=True, hide_index=True)
        else:
            st.info("Silakan atur parameter pada sidebar, lalu tekan tombol **Jalankan Analisis Prediksi**.")

# --- 7. ROUTING (HEART DISEASE DEFAULT) ---
if app_mode == "❤️ Heart Disease Assessment":
    heart_page()
else:
    iris_page()