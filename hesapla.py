import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Hataları daha iyi görmek için config
st.set_page_config(page_title="PrintLab Hata Ayıklama")

def get_sheet():
    # 1. Adım: Secrets okunabiliyor mu?
    if "gcp_service_account" not in st.secrets:
        return "HATA: 'gcp_service_account' bilgisi Secrets içinde bulunamadı!"
    
    creds_dict = st.secrets["gcp_service_account"]
    
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        # 2. Adım: Dosyaya erişilebiliyor mu?
        sh = client.open_by_key("1kafLg6JbF77KW6wtSysG-SX-1eL0uyP34HzWt2nbra")
        return sh.sheet1
    except Exception as e:
        return f"HATA: {str(e)}"

st.title("🖨️ PrintLab Bağlantı Testi")
sonuc = get_sheet()
st.write(sonuc)
