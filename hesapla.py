import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Bağlantısı
def connect_to_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("PrintLab_Data").sheet1
    # Verileri okuma (Sheets'ten veriyi çeker)
def load_data():
    sheet = connect_to_sheet()
    rows = sheet.get_all_records()
    # Sheets'teki satırları, senin eski renkler.json yapına çevirir
    return {row["Filament Adı"]: {"fiyat": float(row["KG Fiyatı"]), "renk": row["Renk"]} for row in rows}

# Verileri yazma (Yeni bir filament eklendiğinde Sheets'e kaydeder)
def save_data(envanter_dict):
    sheet = connect_to_sheet()
    sheet.clear()
    sheet.append_row(["Filament Adı", "KG Fiyatı", "Renk"])
    for isim, veri in envanter_dict.items():
        sheet.append_row([isim, veri["fiyat"], veri["renk"]])
        # ------------------ SESSION STATE ------------------
if "envanter" not in st.session_state:
    try:
        st.session_state.envanter = load_data()
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        st.session_state.envanter = {}
        # ------------------ ARAYÜZ (ARABANIN GÖVDESİ) ------------------
st.subheader("🛠️ Filament Yönetimi")
c1, c2, c3, c4 = st.columns([2,2,1,1])
isim = c1.text_input("Filament Adı")
fiyat = c2.number_input("KG Fiyatı", min_value=0.0)
renk = c3.color_picker("Renk")

if c4.button("EKLE"):
    if isim:
        st.session_state.envanter[isim] = {"fiyat": fiyat, "renk": renk}
        save_data(st.session_state.envanter) # Artık Sheets'e kaydeder!
        st.rerun()

# Listeleme ve Silme
for key, val in list(st.session_state.envanter.items()):
    r1, r2, r3, r4 = st.columns([3,2,2,1])
    r1.write(f"🔹 **{key}**")
    r2.write(f"{val['fiyat']} TL/KG")
    r3.markdown(f"<div style='background:{val['renk']}; height:10px;'></div>", unsafe_allow_html=True)
    if r4.button("❌", key=f"del_{key}"):
        del st.session_state.envanter[key]
        save_data(st.session_state.envanter) # Artık Sheets'ten siler!
        st.rerun()
