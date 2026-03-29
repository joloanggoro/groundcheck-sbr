import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Groundcheck SBR Lampung Tengah", page_icon="📍")

# --- KONEKSI GOOGLE SHEETS ---
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Di Streamlit Cloud, nanti kita pakai st.secrets, tapi untuk lokal pakai file JSON
    path_json = "kunci_api.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(path_json, scope)
    client = gspread.authorize(creds)
    return client.open("Data Groundcheck SBR").sheet1

# --- DATA WILAYAH ---
desa_list = {
    'ANAK RATU AJI': ['BANDAR PUTIH TUA', 'GEDUNG RATU', 'GEDUNG SARI'],
    'ANAK TUHA': ['BUMI AJI', 'BUMI JAYA', 'GUNUNG AGUNG'],
    'GUNUNG SUGIH': ['BUYUT ILIR', 'GUNUNG SUGIH', 'SEPUTIH JAYA'],
    'TERBANGGI BESAR': ['ADI JAYA', 'BANDAR JAYA', 'YUKUM JAYA']
}

# --- TAMPILAN WEB ---
st.title("Pendataan Usaha Tambahan")
st.subheader("Groundcheck SBR Kabupaten Lampung Tengah")
st.info("Isi formulir di bawah dan unggah foto lokasi usaha")

with st.form("form_sbr"):
    nama_usaha = st.text_input("Nama Usaha *")
    nama_pemilik = st.text_input("Nama Pemilik *")
    
    col1, col2 = st.columns(2)
    with col1:
        lon = st.text_input("Longitude")
    with col2:
        lat = st.text_input("Latitude")
    
    alamat = st.text_area("Alamat Lengkap")
    
    kec = st.selectbox("Kecamatan", options=list(desa_list.keys()))
    des = st.selectbox("Desa / Kelurahan", options=desa_list[kec])
    
    catatan = st.text_input("Catatan Tambahan (Contoh: Jual Sembako)")
    
    foto = st.file_uploader("Foto Lokasi Usaha *", type=['jpg', 'png', 'jpeg'])
    
    submit = st.form_submit_button("KIRIM DATA")

# --- PROSES SIMPAN ---
if submit:
    if not nama_usaha or not foto:
        st.error("Nama Usaha dan Foto wajib diisi!")
    else:
        try:
            sheet = connect_sheets()
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                nama_usaha,
                nama_pemilik,
                lon,
                lat,
                alamat,
                kec,
                des,
                catatan,
                "Foto terunggah ke sistem" # Untuk foto di web biasanya diupload ke Google Drive/Cloud
            ]
            sheet.append_row(row)
            st.success("✅ Data berhasil dikirim ke Google Sheets!")
            st.balloons()
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")