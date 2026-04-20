import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="PrintLab | Analiz", page_icon="🖨️")

def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # Hata durumunu netleştirmek için dosya adını kontrol edelim
    return client.open("PrintLab_Data").sheet1

# Verileri Yükle
if "envanter" not in st.session_state:
    try:
        sheet = get_sheet()
        rows = sheet.get_all_records()
        st.session_state.envanter = {row["Filament Adı"]: {"fiyat": row["KG Fiyatı"], "renk": row["Renk"]} for row in rows}
    except:
        st.session_state.envanter = {}

st.title("🖨️ PrintLab Üretim Paneli")

# Filament Ekleme
with st.form("yeni_ekle"):
    col1, col2, col3 = st.columns(3)
    isim = col1.text_input("Filament Adı")
    fiyat = col2.number_input("KG Fiyatı", 0.0)
    renk = col3.color_picker("Renk")
    if st.form_submit_button("EKLE"):
        if isim:
            st.session_state.envanter[isim] = {"fiyat": fiyat, "renk": renk}
            # Sheets'e kaydet
            sheet = get_sheet()
            sheet.clear()
            sheet.append_row(["Filament Adı", "KG Fiyatı", "Renk"])
            for k, v in st.session_state.envanter.items():
                sheet.append_row([k, v['fiyat'], v['renk']])
            st.rerun()

# Listeleme
for key, val in st.session_state.envanter.items():
    st.write(f"🔹 **{key}** | {val['fiyat']} TL/KG")
