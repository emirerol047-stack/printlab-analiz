def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # ID ile doğrudan açıyoruz
    sh = client.open_by_key("1kafLg6JbF77KW6wtSysG-SX-1eL0uyP34HzWt2nbra")
    
    # Sayfa adını net bir şekilde alalım
    return sh.sheet1
