import streamlit as st
import json
import os

# ------------------ AYARLAR ------------------
st.set_page_config(
    page_title="PrintLab | Analiz",
    page_icon="🖨️",
    layout="wide"
)

DB_FILE = "renkler.json"
ELEKTRIK_SAATLIK = 2.5  # TL

# ------------------ VERİ YÖNETİMİ ------------------
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ------------------ SESSION ------------------
if "envanter" not in st.session_state:
    st.session_state.envanter = load_data()

# ------------------ CSS ------------------
st.markdown("""
<style>
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #0f172a;
}
.main-box {
    background: rgba(255,255,255,0.03);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
}
.card {
    background: rgba(30,41,59,0.7);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}
.envanter-box {
    background: rgba(255,255,255,0.02);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='main-box'><h1>🖨️ PrintLab Üretim Paneli</h1></div>", unsafe_allow_html=True)

# ------------------ ENVANTER ------------------
st.subheader("🛠️ Filament Yönetimi")

c1, c2, c3, c4 = st.columns([2,2,1,1])
isim = c1.text_input("Filament Adı")
fiyat = c2.number_input("KG Fiyatı", min_value=0.0)
renk = c3.color_picker("Renk")

if c4.button("EKLE", use_container_width=True):
    if isim:
        st.session_state.envanter[isim] = {
            "fiyat": fiyat,
            "renk": renk
        }
        save_data(st.session_state.envanter)
        st.rerun()
    else:
        st.warning("İsim boş olamaz")

if st.session_state.envanter:
    st.markdown("<div class='envanter-box'>", unsafe_allow_html=True)

    for key, val in list(st.session_state.envanter.items()):
        r1, r2, r3, r4 = st.columns([3,2,2,1])
        r1.write(f"🔹 **{key}**")
        r2.write(f"{val['fiyat']} TL/KG")
        r3.markdown(
            f"<div style='background:{val['renk']}; height:10px; border-radius:5px;'></div>",
            unsafe_allow_html=True
        )

        if r4.button("❌", key=f"del_{key}"):
            del st.session_state.envanter[key]
            save_data(st.session_state.envanter)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------ ÜRETİM ------------------
st.subheader("🎨 Üretim Seçimi")

secilenler = []
gramlar = {}

cols = st.columns(4)

for i, (isim, veri) in enumerate(st.session_state.envanter.items()):
    with cols[i % 4]:

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                padding:6px;
                border-radius:6px;
                background:rgba(255,255,255,0.03);
                margin-bottom:5px;
            ">
                <div style="
                    width:14px;
                    height:14px;
                    background:{veri['renk']};
                    border-radius:4px;
                    border:1px solid rgba(255,255,255,0.2);
                "></div>
            """,
            unsafe_allow_html=True
        )

        if st.checkbox(isim, key=f"chk_{isim}"):
            secilenler.append(isim)

        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ ANALİZ ------------------
if secilenler:
    st.divider()

    g_cols = st.columns(len(secilenler))

    for i, s in enumerate(secilenler):
        with g_cols[i]:
            gramlar[s] = st.number_input(f"{s} (gr)", min_value=0.0)

    c1, c2 = st.columns(2)
    adet = c1.number_input("Adet", min_value=1, value=1)
    saat = c2.number_input("Baskı Süresi (Saat)", min_value=0.0, value=1.0)

    if st.button("🚀 ANALİZİ GÖSTER", use_container_width=True):

        toplam = 0
        for s in secilenler:
            kg_fiyat = st.session_state.envanter[s]["fiyat"]
            toplam += (kg_fiyat / 1000) * gramlar[s]

        elektrik = saat * ELEKTRIK_SAATLIK
        birim_maliyet = (toplam + elektrik) / adet

        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='card'><h4>%100 Kâr</h4><h2>{birim_maliyet*2:.2f} TL</h2></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='card'><h4>%120 Kâr</h4><h2>{birim_maliyet*2.2:.2f} TL</h2></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='card'><h4>%140 Kâr</h4><h2>{birim_maliyet*2.4:.2f} TL</h2></div>", unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("""
<hr>
<div style='text-align:right'>
<a href="https://www.instagram.com/printlab_3dstore/" target="_blank"
style="color:white;text-decoration:none; display:flex; align-items:center; justify-content:flex-end; gap:8px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="20">
    <b>@printlab_3dstore</b>
</a>
</div>
""", unsafe_allow_html=True)