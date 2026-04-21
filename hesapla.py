import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="PrintLab | Analiz", page_icon="🖨️")

def get_sheet():
    # Secrets'tan bilgileri çekiyoruz
    creds_dict = st.secrets["gcp_service_account"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # Tabloyu ID ile açıyoruz
    sh = client.open_by_key("1kafLg6JbF77KW6wtSysG-SX-1eL0uyP34HzWt2nbra")
    return sh.sheet1

st.title("🖨️ PrintLab Üretim Paneli")

try:
    sheet = get_sheet()
    st.success("Bağlantı başarılı!")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
