import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="PrintLab | Analiz", page_icon="🖨️", layout="wide")

def connect_to_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("PrintLab_Data").sheet1

def load_data():
    sheet = connect_to_sheet()
    rows = sheet.get_all_records()
    return {row["Filament Adı"]: {"fiyat": float(row["KG Fiyatı"]), "renk": row["Renk"]} for row in rows}

def save_data(data):
    sheet = connect_to_sheet()
    sheet.clear()
    sheet.append_row(["Filament Adı", "KG Fiyatı", "Renk"])
    for isim, veri in data.items():
        sheet.append_row([isim, veri["fiyat"], veri["renk"]])

if "envanter" not in st.session_state:
    st.session_state.envanter = load_data()

st.title("🖨️ PrintLab Üretim Paneli")

# Filament Ekleme Bölümü
st.subheader("🛠️ Yeni Filament Ekle")
c1, c2, c3, c4 = st.columns([2,2,1,1])
isim = c1.text_input("Filament Adı", key="yeni_isim")
fiyat = c2.number_input("KG Fiyatı", min_value=0.0, key="yeni_fiyat")
renk = c3.color_picker("Renk", key="yeni_renk")

if c4.button("EKLE"):
    if isim:
        st.session_state.envanter[isim] = {"fiyat": fiyat, "renk": renk}
        save_data(st.session_state.envanter)
        st.rerun()

# Listeleme Bölümü
st.subheader("📦 Mevcut Envanter")
for key, val in list(st.session_state.envanter.items()):
    r1, r2, r3, r4 = st.columns([3,2,2,1])
    r1.write(f"🔹 **{key}**")
    r2.write(f"{val['fiyat']} TL/KG")
    r3.markdown(f"<div style='background:{val['renk']}; height:10px;'></div>", unsafe_allow_html=True)
    if r4.button("❌", key=f"del_{key}"):
        del st.session_state.envanter[key]
        save_data(st.session_state.envanter)
        st.rerun()
