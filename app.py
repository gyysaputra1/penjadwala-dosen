import streamlit as st
import pandas as pd

st.set_page_config(page_title="Penjadwalan Dosen", layout="wide")
st.title("📚 Aplikasi Mini Penjadwalan Dosen")

uploaded_file = st.file_uploader("Upload file Excel jadwal (.xlsx)", type=["xlsx"])

if uploaded_file:
    excel_data = pd.ExcelFile(uploaded_file)
    sheet_names = excel_data.sheet_names
    st.success(f"Sheet ditemukan: {sheet_names}")

    df = pd.read_excel(uploaded_file, sheet_name="Mapping mata kuliah", skiprows=2)
    
    st.subheader("📦 Data Mentah (Raw dari Excel)")
    st.dataframe(df.head(10))

    df = df.rename(columns={
        df.columns[1]: "Nama Dosen",
        df.columns[2]: "Mata Kuliah",
        df.columns[3]: "Semester",
        df.columns[4]: "SKS",
        df.columns[5]: "Kelas",
        df.columns[6]: "Hari",
        df.columns[7]: "Jam",
        
        })

    df[["Nama Dosen", "Mata Kuliah", "Semester", "SKS"]] = df[["Nama Dosen", "Mata Kuliah", "Semester", "SKS"]].fillna(method='ffill')

    df["Jam"] = df["Jam"].astype(str).str.replace("nan", "").str.strip()

    hari_valid = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    df = df[df["Hari"].isin(hari_valid)]

    st.subheader("🧹 Data Jadwal (Hasil Bersih)")
    st.dataframe(df[["Nama Dosen", "Mata Kuliah", "Kelas", "Hari", "Jam"]])
   
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    jam_list = sorted(df["Jam"].unique())
    
    from io import BytesIO

if st.button("📊 Proses Jadwal Mingguan"):
    hari_list = hari_valid
    jam_list = sorted(df["Jam"].unique())
    tabel_jadwal = {hari: {jam: [] for jam in jam_list} for hari in hari_list}

    for i, row in df.iterrows():
        dosen = row["Nama Dosen"]
        matkul = row["Mata Kuliah"]
        kelas = row["Kelas"]
        hari = row["Hari"]
        jam = row["Jam"]
        
    jadwal_mingguan = {
        jam: [", ".join(tabel_jadwal[hari][jam]) for hari in hari_list]
        for jam in jam_list
    }

    jadwal_df = pd.DataFrame(jadwal_mingguan, index=hari_list)

    st.subheader("🗓️ Jadwal Mengajar Mingguan")
    st.dataframe(jadwal_df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        jadwal_df.to_excel(writer, index=True)
    output.seek(0)

    st.download_button(
        label="⬇️ Download Jadwal Mingguan sebagai Excel",
        data=output,
        file_name="Jadwal_Mingguan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.subheader("🚨 Deteksi Jadwal Bentrok Dosen")
    bentrok = []

    for hari in hari_list:
        for jam in jam_list:
            sesi = tabel_jadwal[hari][jam]
            dosen_aktif = []
            for entry in sesi:
                if "(" in entry:
                    nama = entry.split("(")[1].split(")")[0].strip()
                    if nama in dosen_aktif:
                        bentrok.append(f"{nama} bentrok pada {hari} jam {jam}")
                    else:
                        dosen_aktif.append(nama)

    if bentrok:
        for b in bentrok:
            st.error(f"❌ {b}")
    else:
        st.success("✅ Tidak ada bentrok dosen!")
