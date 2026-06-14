import streamlit as st

st.set_page_config(
    page_title="Kalkulator Resistor",
    page_icon="🔌",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,0.35), transparent 30%),
        radial-gradient(circle at bottom right, rgba(59,130,246,0.35), transparent 35%),
        linear-gradient(135deg, #020617, #0f172a, #1e1b4b);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.38);
    backdrop-filter: blur(10px);
}

.result-box {
    background: linear-gradient(135deg, #22c55e, #15803d);
    padding: 24px;
    border-radius: 22px;
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: white;
    margin-top: 25px;
    box-shadow: 0 12px 30px rgba(34,197,94,0.35);
}

.formula-box {
    background: rgba(15,23,42,0.75);
    border-left: 5px solid #38bdf8;
    padding: 18px;
    border-radius: 16px;
    margin-top: 18px;
    color: #e2e8f0;
    font-size: 18px;
}

.resistor-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 35px 0;
}

.lead {
    width: 110px;
    height: 7px;
    background: linear-gradient(90deg, #64748b, #e2e8f0, #64748b);
    border-radius: 999px;
}

.resistor {
    width: 340px;
    height: 105px;
    background: linear-gradient(90deg, #8a4f0a, #f6d365, #ffd98a, #f6d365, #8a4f0a);
    border-radius: 48% / 58%;
    border: 4px solid #7c4a03;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    box-shadow:
        inset 0 10px 18px rgba(255,255,255,0.42),
        inset 0 -12px 18px rgba(0,0,0,0.30),
        0 16px 35px rgba(0,0,0,0.45);
}

.band {
    width: 22px;
    height: 96px;
    border-radius: 8px;
    border: 1px solid rgba(0,0,0,0.35);
    box-shadow:
        inset 0 0 8px rgba(0,0,0,0.45),
        0 0 8px rgba(255,255,255,0.2);
}

.info-card {
    background: rgba(15,23,42,0.78);
    border-radius: 22px;
    padding: 22px;
    border: 1px solid rgba(148,163,184,0.3);
    margin-bottom: 18px;
}

.big-icon {
    font-size: 38px;
}

.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(56,189,248,0.18);
    color: #bae6fd;
    border: 1px solid rgba(56,189,248,0.35);
    margin: 4px;
    font-weight: 700;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.18);
}
</style>
""", unsafe_allow_html=True)

colors = {
    "Hitam": ("#111111", 0),
    "Coklat": ("#7c3f00", 1),
    "Merah": ("#dc2626", 2),
    "Oranye": ("#f97316", 3),
    "Kuning": ("#facc15", 4),
    "Hijau": ("#16a34a", 5),
    "Biru": ("#2563eb", 6),
    "Ungu": ("#7c3aed", 7),
    "Abu-abu": ("#9ca3af", 8),
    "Putih": ("#ffffff", 9),
}

tol_colors = {
    "Coklat ±1%": ("#7c3f00", 1),
    "Merah ±2%": ("#dc2626", 2),
    "Emas ±5%": ("#d4af37", 5),
    "Perak ±10%": ("#c0c0c0", 10),
}

components = {
    "LED kecil": {
        "emoji": "💡",
        "volt": "3V - 5V",
        "battery": "2x AA / 3x AA / USB 5V",
        "note": "Wajib pakai resistor, biasanya 220Ω sampai 330Ω."
    },
    "Buzzer aktif": {
        "emoji": "🔊",
        "volt": "3V - 5V",
        "battery": "3x AA atau USB 5V",
        "note": "Cocok untuk Arduino, tinggal sambung ke pin digital."
    },
    "Servo SG90": {
        "emoji": "⚙️",
        "volt": "5V",
        "battery": "4x AA lebih aman daripada baterai 9V kotak",
        "note": "Servo butuh arus lumayan besar. Jangan pakai dari pin 5V Arduino kalau bebannya berat."
    },
    "HC-SR04 Ultrasonic": {
        "emoji": "📡",
        "volt": "5V",
        "battery": "USB 5V / powerbank / 4x AA lewat regulator",
        "note": "VCC ke 5V, GND ke GND, trig/echo ke pin digital."
    },
    "Arduino UNO": {
        "emoji": "🟦",
        "volt": "5V logic / 7V - 12V jack input",
        "battery": "USB powerbank paling enak, atau adaptor 9V",
        "note": "Kalau lewat USB cukup 5V. Kalau lewat jack bulat biasanya 7-12V."
    },
    "ESP32": {
        "emoji": "📶",
        "volt": "5V USB / 3.3V logic",
        "battery": "Powerbank 5V atau baterai Li-ion + module charger/regulator",
        "note": "Pin ESP32 kebanyakan 3.3V, jangan asal kasih sinyal 5V."
    },
    "Relay 5V": {
        "emoji": "🔁",
        "volt": "5V",
        "battery": "USB 5V / adaptor 5V",
        "note": "Relay boros arus. Lebih aman pakai supply 5V terpisah."
    },
    "LCD I2C 16x2": {
        "emoji": "🖥️",
        "volt": "5V",
        "battery": "USB 5V / powerbank",
        "note": "SDA/SCL ke pin I2C Arduino, VCC ke 5V."
    },
}

def format_ohm(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    if value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    return f"{value:g} Ω"

st.markdown("<div class='main-title'>🔌 Kalkulator Resistor Deluxe</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Pilih warna gelang resistor + cek kebutuhan volt komponen elektronik.</div>", unsafe_allow_html=True)

left, right = st.columns([1.25, 1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎨 Kode Warna Resistor")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        band1 = st.selectbox("Gelang 1", list(colors.keys()), index=1)
    with c2:
        band2 = st.selectbox("Gelang 2", list(colors.keys()), index=0)
    with c3:
        mult = st.selectbox("Pengali", list(colors.keys()), index=2)
    with c4:
        tol = st.selectbox("Toleransi", list(tol_colors.keys()), index=2)

    b1_hex, b1_val = colors[band1]
    b2_hex, b2_val = colors[band2]
    m_hex, m_val = colors[mult]
    t_hex, t_val = tol_colors[tol]

    nilai = (b1_val * 10 + b2_val) * (10 ** m_val)
    hasil = format_ohm(nilai)

    st.markdown(f"""
    <div class="resistor-wrap">
        <div class="lead"></div>
        <div class="resistor">
            <div class="band" style="background:{b1_hex};"></div>
            <div class="band" style="background:{b2_hex};"></div>
            <div class="band" style="background:{m_hex};"></div>
            <div class="band" style="background:{t_hex};"></div>
        </div>
        <div class="lead"></div>
    </div>

    <div class="result-box">
        {hasil} &nbsp; | &nbsp; Toleransi ±{t_val}%
    </div>

    <div class="formula-box">
        Rumus: ({b1_val}{b2_val}) × 10<sup>{m_val}</sup> = {nilai:g} Ω
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔋 Cek Volt Komponen")

    selected = st.selectbox("Pilih komponen", list(components.keys()))
    comp = components[selected]

    st.markdown(f"""
    <div class="info-card">
        <div class="big-icon">{comp["emoji"]}</div>
        <h2>{selected}</h2>
        <span class="badge">Volt: {comp["volt"]}</span>
        <span class="badge">Baterai: {comp["battery"]}</span>
        <hr>
        <p>{comp["note"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning("Catatan: volt harus sesuai komponen. Baterai 9V kotak kurang cocok untuk servo/motor karena arusnya kecil.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h3>⚡ Tips Cepat</h3>
<p>
🔴 5V biasanya untuk Arduino UNO, HC-SR04, servo SG90, relay 5V, LCD I2C.<br>
🔵 3.3V biasanya untuk ESP32 bagian pin logic.<br>
🟢 Untuk project sekolah, powerbank 5V sering paling aman dan gampang.
</p>
</div>
""", unsafe_allow_html=True)