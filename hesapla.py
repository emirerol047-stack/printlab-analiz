import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("🖨️ PrintLab Detaylı Bağlantı Testi")

try:
    # 1. Secrets kontrolü
    if "gcp_service_account" not in st.secrets:
        st.error("HATA: Secrets içinde 'gcp_service_account' bulunamadı.")
    else:
        creds_dict = st.secrets["gcp_service_account"]
        st.write("1. Secrets okundu.")
        
        # 2. Yetkilendirme
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        st.write("2. Yetkilendirme başarılı.")
        
        # 3. Tablo erişimi
        sh = client.open_by_key("1kafLg6JbF77KW6wtSysG-SX-1eL0uyP34HzWt2nbra")
        st.write("3. Tablo bulundu: " + sh.title)
        
        # 4. Sekme erişimi
        ws = sh.sheet1
        st.success(f"4. Bağlantı TAMAM! '{ws.title}' sayfasına ulaşıldı.")

except Exception as e:
    st.error(f"HATA OLUŞTU: {type(e).__name__} - {e}")
