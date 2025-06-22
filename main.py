import pandas as pd

file_path = "MAPPING JADWAL MENGAJAR TEKNIK INFORMATIKA .xlsx"

excel_data = pd.ExcelFile(file_path)
print("Sheet yang ditemukan:")
print(excel_data.sheet_names)

df = pd.read_excel(file_path, sheet_name="Mapping mata kuliah", skiprows=2)

print("\nData awal:")
print(df.head(10))
df = df.rename(columns={
    df.columns[0]: "Nama Dosen",
    df.columns[1]: "Mata Kuliah",
    df.columns[2]: "Semester",
    df.columns[3]: "SKS",
    df.columns[4]: "Kelas",
    df.columns[5]: "Hari",
    df.columns[6]: "Jam_1",
    df.columns[7]: "Jam_2"
})

df[["Nama Dosen", "Mata Kuliah", "Semester", "SKS"]] = df[["Nama Dosen", "Mata Kuliah", "Semester", "SKS"]].fillna(method='ffill')

df["Jam"] = df["Jam_1"].astype(str).str.strip() + " " + df["Jam_2"].astype(str).str.strip()
df["Jam"] = df["Jam"].str.replace("nan", "").str.strip()

hari_valid = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
df = df[df["Hari"].isin(hari_valid)]


print("\nData yang sudah dibersihkan:")
print(df[["Nama Dosen", "Mata Kuliah", "Kelas", "Hari", "Jam"]].head(10))


print("\nData yang sudah dibersihkan:")
print(df[["Nama Dosen", "Mata Kuliah", "Kelas", "Hari", "Jam"]].head(10))

hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
jam_list = sorted(df["Jam"].unique())

tabel_jadwal = {hari: {jam: [] for jam in jam_list} for hari in hari_list}

for i, row in df.iterrows():
    dosen = row["Nama Dosen"]
    matkul = row["Mata Kuliah"]
    kelas = row["Kelas"]
    hari = row["Hari"]
    jam = row["Jam"]
    info = f"{matkul} ({dosen}) - {kelas}"
    if info not in tabel_jadwal[hari][jam]:
        tabel_jadwal[hari][jam].append(info)

jadwal_mingguan = {
    jam: [", ".join(tabel_jadwal[hari][jam]) for hari in hari_list]
    for jam in jam_list
}

import pandas as pd
jadwal_df = pd.DataFrame(jadwal_mingguan, index=hari_list)

print("\nJadwal Mingguan (contoh):")
print(jadwal_df.head())
jadwal_df.to_excel("Jadwal_Mingguan_Dosen.xlsx")
print("Jadwal disimpan ke file: Jadwal_Mingguan_Dosen.xlsx")

bentrok = []

for hari in hari_list:
    for jam in jam_list:
        sesi = tabel_jadwal[hari][jam]
        dosen_terpakai = []
        for entry in sesi:
            if "(" in entry:
                nama = entry.split("(")[1].split(")")[0].strip()
                if nama in dosen_terpakai:
                    bentrok.append(f"BENTROK: {nama} pada {hari} jam {jam}")
                else:
                    dosen_terpakai.append(nama)

if bentrok:
    print("\n Jadwal Bentrok Ditemukan:")
    for b in bentrok:
        print("-", b)
else:
    print("\n✅ Tidak ada bentrok dosen!")

jadwal_per_dosen = {}

for i, row in df.iterrows():
    dosen = row["Nama Dosen"]
    hari = row["Hari"]
    jam = row["Jam"]
    matkul = row["Mata Kuliah"]
    kelas = row["Kelas"]
    info = f"{hari} - {jam} : {matkul} ({kelas})"
    if dosen not in jadwal_per_dosen:
        jadwal_per_dosen[dosen] = []
    jadwal_per_dosen[dosen].append(info)

print("\n📋 Jadwal Per Dosen:")
for dosen, jadwal in jadwal_per_dosen.items():
    print(f"\n{dosen}")
    for item in jadwal:
        print(" •", item)
data_export = []

for dosen, jadwal in jadwal_per_dosen.items():
    for item in jadwal:
        hari, sisanya = item.split(" - ")
        jam, detail = sisanya.split(" : ")
        matkul, kelas = detail.strip().split(" (")
        kelas = kelas.replace(")", "")
        data_export.append([dosen, hari.strip(), jam.strip(), matkul.strip(), kelas.strip()])

df_dosen = pd.DataFrame(data_export, columns=["Dosen", "Hari", "Jam", "Mata Kuliah", "Kelas"])
df_dosen.to_excel("Jadwal_Per_Dosen.xlsx", index=False)
print("\n✅ Jadwal per dosen disimpan ke: Jadwal_Per_Dosen.xlsx")
