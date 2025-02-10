import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt

# Mengatur tema seaborn
sns.set(style='whitegrid')

# Membaca dataset
days_df = pd.read_csv("day_clean.csv")
hours_df = pd.read_csv("hour_clean.csv")

# Konversi kolom tanggal ke tipe datetime
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Rentang tanggal minimal dan maksimal
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

# Sidebar untuk filter rentang waktu
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    st.header("📆 Pilih Rentang Waktu")
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# Konversi tanggal input ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan tanggal
main_df_days = days_df[(days_df["dteday"] >= start_date) & (days_df["dteday"] <= end_date)]

# Menghitung metrik utama
total_sharing = main_df_days["cnt"].sum()
total_registered = main_df_days["registered"].sum()
total_casual = main_df_days["casual"].sum()

# Header utama dashboard
st.title('🚴‍♂️ Bike Sharing Dashboard')
st.markdown("---")

# Menampilkan metrik utama
total_col1, total_col2, total_col3 = st.columns(3)
with total_col1:
    st.metric("Total Penyewaan", value=total_sharing)
with total_col2:
    st.metric("Pengguna Terdaftar", value=total_registered)
with total_col3:
    st.metric("Pengguna Casual", value=total_casual)

st.markdown("---")

# 1. Perbandingan Penyewaan Sepeda 2011 vs 2012
st.subheader("📊 Perbandingan Peminjaman Sepeda antara 2011 dan 2012")
yearly_rentals = days_df.groupby(days_df["dteday"].dt.year)["cnt"].sum()
fig1, ax1 = plt.subplots()
yearly_rentals.plot(kind='bar', color=["#4753a4", "#9c1d3b"], ax=ax1)
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Total Peminjaman Sepeda")
st.pyplot(fig1)

# 2. Tren Penyewaan Sepeda per Bulan
st.subheader("📆 Tren Penyewaan Sepeda per Bulan")
monthly_rentals = days_df.groupby(days_df["dteday"].dt.month)["cnt"].sum().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(x=monthly_rentals["dteday"], y=monthly_rentals["cnt"], palette="Blues", ax=ax2)
ax2.set_xticks(range(12))
ax2.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.pyplot(fig2)

# 3. Tren Penyewaan Sepeda Harian
st.subheader("📈 Tren Penyewaan Sepeda Harian")
chart = alt.Chart(main_df_days).mark_line(point=True).encode(
    x='dteday:T',
    y='cnt:Q',
    tooltip=['dteday', 'cnt']
).interactive()
st.altair_chart(chart, use_container_width=True)

# 4. Pengaruh Cuaca terhadap Peminjaman Sepeda
st.subheader("🌦️ Pengaruh Cuaca terhadap Peminjaman Sepeda")
weather_rentals = days_df.groupby("weathersit")["cnt"].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(x=weather_rentals["weathersit"], y=weather_rentals["cnt"], palette=["#A7C7E7", "#D3D3D3", "#E57373"], ax=ax3)
st.pyplot(fig3)

st.markdown("---")
st.markdown("📊 **Kesimpulan**")
st.write("Dashboard menunjukkan tren peminjaman sepeda berdasarkan faktor cuaca, bulan, dan pengguna terdaftar vs casual.")

