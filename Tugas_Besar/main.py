import streamlit as st
from manager import LogistikManager
import pandas as pd

# Initialize LogistikManager
manager = LogistikManager("logistik.db")

# Set page configuration
st.set_page_config(
    page_title="Sistem Manajemen Logistik", 
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚛 Navigasi")
menu = ["Dashboard", "Manajemen Barang", "Manajemen Gudang", "Manajemen Transaksi", "Manajemen Stok"]
choice = st.sidebar.selectbox("Pilih Menu", menu)

# Dashboard
if choice == "Dashboard":
    # Header dengan styling
    st.markdown("""
    <div class="main-header">
        <h1>📦 Dashboard Logistik</h1>
        <p>Sistem Manajemen Gudang dan Inventori</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ringkasan Stok
    ringkasan = manager.get_ringkasan_stok()
    if "error" not in ringkasan:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Barang</h3>
                <h2>{ringkasan["total_barang"]}</h2>
                <p>Jenis tersedia</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Gudang</h3>
                <h2>{ringkasan["total_gudang"]}</h2>
                <p>Lokasi aktif</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Item</h3>
                <h2>{ringkasan["total_item_stok"]}</h2>
                <p>Item dalam stok</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Nilai Stok</h3>
                <h2>Rp {ringkasan['total_nilai_stok']:,.0f}</h2>
                <p>Total investasi</p>
            </div>
            """, unsafe_allow_html=True)
        
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("Kapasitas Total", ringkasan["total_kapasitas"])
        with col6:
            st.metric("Kapasitas Terpakai", ringkasan["total_terpakai"])
        with col7:
            st.metric("Persentase Terpakai", f"{ringkasan['persentase_terpakai']:.2f}%")
    
    # Barang dengan Stok Rendah
    st.subheader("⚠️ Barang dengan Stok Rendah")
    stok_rendah = manager.get_barang_stok_rendah(batas_minimum=10)
    if stok_rendah:
        df_stok_rendah = pd.DataFrame(stok_rendah)
        st.dataframe(df_stok_rendah)
        st.markdown("""
        <div class="error-box">
            <strong>❌ Peringatan!</strong> Ada barang dengan stok rendah yang perlu segera di-restock.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <strong>✅ Baik!</strong> Semua barang memiliki stok yang mencukupi.
        </div>
        """, unsafe_allow_html=True)
    
    # Gudang Hampir Penuh
    st.subheader("📦 Gudang Hampir Penuh")
    gudang_penuh = manager.get_gudang_hampir_penuh(persentase_batas=80.0)
    if gudang_penuh:
        df_gudang_penuh = pd.DataFrame(gudang_penuh)
        st.dataframe(df_gudang_penuh)
        st.markdown("""
        <div class="error-box">
            <strong>❌ Peringatan!</strong> Ada gudang yang hampir penuh, pertimbangkan untuk ekspansi atau redistribusi.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <strong>✅ Baik!</strong> Semua gudang memiliki kapasitas yang mencukupi.
        </div>
        """, unsafe_allow_html=True)
    
    # Histori Transaksi
    st.subheader("📊 Histori Transaksi Terbaru")
    transaksi = manager.get_histori_transaksi(limit=10)
    if transaksi:
        df_transaksi = pd.DataFrame(transaksi, columns=["ID", "Nama Barang", "Nama Gudang", "Jenis", "Jumlah", "Tanggal", "Keterangan"])
        st.dataframe(df_transaksi)
    else:
        st.info("Belum ada transaksi.")

# Manajemen Barang
elif choice == "Manajemen Barang":
    st.title("📋 Manajemen Barang")
    
    # Form Tambah Barang
    with st.form("form_tambah_barang"):
        st.subheader("➕ Tambah Barang Baru")
        nama = st.text_input("Nama Barang")
        kategori = st.text_input("Kategori")
        satuan = st.text_input("Satuan")
        harga_satuan = st.number_input("Harga Satuan (Rp)", min_value=0.0)
        deskripsi = st.text_area("Deskripsi")
        submit_barang = st.form_submit_button("Tambah Barang")
        
        if submit_barang:
            result = manager.tambah_barang(nama, kategori, satuan, harga_satuan, deskripsi)
            if result["success"]:
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Berhasil!</strong> {result["message"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-box">
                    <strong>❌ Gagal!</strong> {result["message"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Daftar Barang
    st.subheader("📦 Daftar Barang")
    barang_list = manager.get_semua_barang()
    if barang_list:
        df_barang = pd.DataFrame([vars(b) for b in barang_list])
        st.dataframe(df_barang)
    else:
        st.info("Belum ada barang terdaftar.")

# Manajemen Gudang
elif choice == "Manajemen Gudang":
    st.title("🏢 Manajemen Gudang")
    
    # Form Tambah Gudang
    with st.form("form_tambah_gudang"):
        st.subheader("➕ Tambah Gudang Baru")
        nama = st.text_input("Nama Gudang")
        lokasi = st.text_input("Lokasi")
        kapasitas_maksimum = st.number_input("Kapasitas Maksimum", min_value=0)
        submit_gudang = st.form_submit_button("Tambah Gudang")
        
        if submit_gudang:
            result = manager.tambah_gudang(nama, lokasi, kapasitas_maksimum)
            if result["success"]:
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Berhasil!</strong> {result["message"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-box">
                    <strong>❌ Gagal!</strong> {result["message"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Daftar Gudang
    st.subheader("🏗️ Daftar Gudang")
    gudang_list = manager.get_semua_gudang()
    if gudang_list:
        df_gudang = pd.DataFrame([vars(g) for g in gudang_list])
        st.dataframe(df_gudang)
    else:
        st.info("Belum ada gudang terdaftar.")

# Manajemen Transaksi
elif choice == "Manajemen Transaksi":
    st.title("🔄 Manajemen Transaksi")
    
    # Form Tambah Transaksi
    with st.form("form_tambah_transaksi"):
        st.subheader("➕ Tambah Transaksi Baru")
        barang_list = manager.get_semua_barang()
        gudang_list = manager.get_semua_gudang()
        
        if not barang_list or not gudang_list:
            st.warning("Pastikan sudah ada barang dan gudang terdaftar sebelum membuat transaksi.")
        else:
            barang_options = {b.nama: b.id for b in barang_list}
            gudang_options = {g.nama: g.id for g in gudang_list}
            
            barang_nama = st.selectbox("Pilih Barang", list(barang_options.keys()))
            gudang_nama = st.selectbox("Pilih Gudang", list(gudang_options.keys()))
            jenis = st.selectbox("Jenis Transaksi", ["masuk", "keluar"])
            jumlah = st.number_input("Jumlah", min_value=1)
            keterangan = st.text_area("Keterangan")
            submit_transaksi = st.form_submit_button("Proses Transaksi")
            
            if submit_transaksi:
                barang_id = barang_options[barang_nama]
                gudang_id = gudang_options[gudang_nama]
                result = manager.proses_transaksi(barang_id, gudang_id, jenis, jumlah, keterangan)
                if result["success"]:
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ Berhasil!</strong> {result["message"]} (Stok Baru: {result["stok_baru"]})
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <strong>❌ Gagal!</strong> {result["message"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Histori Transaksi
    st.subheader("📊 Histori Transaksi")
    transaksi = manager.get_histori_transaksi()
    if transaksi:
        df_transaksi = pd.DataFrame(transaksi, columns=["ID", "Nama Barang", "Nama Gudang", "Jenis", "Jumlah", "Tanggal", "Keterangan"])
        st.dataframe(df_transaksi)
    else:
        st.info("Belum ada transaksi.")

# Manajemen Stok
elif choice == "Manajemen Stok":
    st.title("📊 Manajemen Stok")
    
    # Daftar Semua Stok
    st.subheader("📋 Daftar Semua Stok")
    stok_list = manager.get_semua_stok()
    if stok_list:
        df_stok = pd.DataFrame(stok_list, columns=["Nama Barang", "Nama Gudang", "Jumlah", "Satuan"])
        st.dataframe(df_stok)
    else:
        st.info("Belum ada stok terdaftar.")
    
    # Stok per Gudang
    st.subheader("🏢 Stok per Gudang")
    gudang_list = manager.get_semua_gudang()
    if gudang_list:
        gudang_options = {g.nama: g.id for g in gudang_list}
        selected_gudang = st.selectbox("Pilih Gudang untuk Melihat Stok", list(gudang_options.keys()))
        
        stok_gudang = manager.get_stok_by_gudang(gudang_options[selected_gudang])
        if stok_gudang:
            df_stok_gudang = pd.DataFrame(stok_gudang, columns=["Nama Barang", "Jumlah", "Satuan", "Kategori"])
            st.dataframe(df_stok_gudang)
        else:
            st.info(f"Tidak ada stok di gudang {selected_gudang}.")
    else:
        st.info("Belum ada gudang terdaftar.")