import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat dataset baru
file_path = "all_data.csv"  # Sesuaikan dengan lokasi file
all_data = pd.read_csv(file_path)

# Memilih kolom yang relevan dari dataset
all_data = all_data.rename(columns={
    "season_x": "season",
    "workingday_x": "workingday",
    "weathersit_x": "weathersit",
    "temp_x": "temp",
    "cnt_x": "cnt",
    "mnth_x": "month",
    "casual_x": "casual",
    "registered_x": "registered"
})

# Mapping musim dan hari kerja
all_data["season_label"] = all_data["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
all_data["workingday_label"] = all_data["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})

# Sidebar
st.sidebar.title("Dashboard Bike Sharing")
st.sidebar.write("Analisis Pola Penyewaan Sepeda")

# **Widget Interaktif**
# Pilih musim
season_selected = st.sidebar.selectbox("Pilih Musim", ["All"] + list(all_data["season_label"].unique()))

# Pilih rentang bulan
month_range = st.sidebar.slider("Pilih Rentang Bulan", 1, 12, (1, 12))

# Pilih tipe pengguna
user_type = st.sidebar.radio("Pilih Tipe Pengguna", ["Semua", "Casual", "Registered"])

# **Filter Data**
filtered_data = all_data.copy()

if season_selected != "All":
    filtered_data = filtered_data[filtered_data["season_label"] == season_selected]

filtered_data = filtered_data[(filtered_data["month"] >= month_range[0]) & (filtered_data["month"] <= month_range[1])]

# **Header Utama**
st.title("📊 Dashboard Bike Sharing")
st.write("Visualisasi pola penggunaan sepeda berdasarkan hari kerja vs akhir pekan dan pola musiman.")

# **Perbandingan Hari Kerja vs Akhir Pekan**
st.subheader("🚲 Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
hourly_trend = filtered_data.groupby(["workingday_label", "hr"])["cnt"].mean().reset_index()
st.write(hourly_trend)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="hr", y="cnt", hue="workingday_label", data=hourly_trend, marker="o", palette=["red", "blue"], ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Perbandingan Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
ax.set_xticks(range(0, 24))
ax.legend(title="Kategori Hari")
ax.grid(True)
st.pyplot(fig)

# **Perbandingan Pola Penyewaan Berdasarkan Musim**
st.subheader("🌤️ Pola Penyewaan Berdasarkan Musim")
season_order = ["Spring", "Summer", "Fall", "Winter"]
season_analysis = filtered_data.groupby("season_label")["cnt"].agg(["mean", "median", "max", "min", "count"]).reindex(season_order)
st.write(season_analysis)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_analysis.index, y=season_analysis["mean"], palette="viridis", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# **Pola Penyewaan Berdasarkan Bulan**
st.subheader("📅 Pola Penyewaan Berdasarkan Bulan")
month_analysis = filtered_data.groupby("month")["cnt"].agg(["mean", "median", "max", "min", "count"])
st.write(month_analysis)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=month_analysis.index, y=month_analysis["mean"], marker="o", color="blue")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Bulan")
st.pyplot(fig)

# **Analisis Penyewaan Berdasarkan Tipe Pengguna**
st.subheader("👥 Perbandingan Pengguna Kasual vs Terdaftar")

if user_type == "Casual":
    user_type_analysis = filtered_data[["casual"]].agg(["mean", "median", "max", "min"])
    st.write(user_type_analysis)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=["Casual"], y=[user_type_analysis.loc["mean", "casual"]], palette="muted", ax=ax)
    ax.set_xlabel("Tipe Pengguna")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Rata-rata Penyewaan: Pengguna Kasual")
    st.pyplot(fig)

elif user_type == "Registered":
    user_type_analysis = filtered_data[["registered"]].agg(["mean", "median", "max", "min"])
    st.write(user_type_analysis)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=["Registered"], y=[user_type_analysis.loc["mean", "registered"]], palette="muted", ax=ax)
    ax.set_xlabel("Tipe Pengguna")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Rata-rata Penyewaan: Pengguna Terdaftar")
    st.pyplot(fig)

else:
    user_type_analysis = filtered_data[["casual", "registered"]].agg(["mean", "median", "max", "min"])
    st.write(user_type_analysis)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=["Casual", "Registered"], y=[user_type_analysis.loc["mean", "casual"], user_type_analysis.loc["mean", "registered"]], palette="muted", ax=ax)
    ax.set_xlabel("Tipe Pengguna")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Rata-rata Penyewaan: Pengguna Kasual vs Terdaftar")
    st.pyplot(fig)

# **Footer**
st.write("\n📌 Data diambil dari dataset Bike Sharing (`all_data.csv`).")
