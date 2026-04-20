def get_sheet():
    # Bağlantıyı şimdilik boş bırakıyoruz ki uygulama açılsın
    return None
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # ID ile doğrudan açıyoruz
    sh = client.open_by_key("1kafLg6JbF77KW6wtSysG-SX-1eL0uyP34HzWt2nbra")
    
    # Sayfa adını net bir şekilde alalım
    return sh.sheet1
