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

# Filter data berdasarkan tanggal
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]

# Menghitung metrik utama
total_sharing = main_df_days["count_cr"].sum()
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
yearly_rentals = days_df.groupby(days_df["dteday"].dt.year)["count_cr"].sum()
fig1, ax1 = plt.subplots()
yearly_rentals.plot(kind='bar', color=["#4753a4", "#9c1d3b"], ax=ax1)
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Total Peminjaman Sepeda")
ax1.set_title("Perbandingan Peminjaman Sepeda antara 2011 dan 2012")
st.pyplot(fig1)

# 2. Tren Penyewaan Sepeda per Bulan
st.subheader("📆 Tren Penyewaan Sepeda per Bulan")
monthly_rentals = days_df.groupby(days_df["dteday"].dt.month)["count_cr"].sum().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(x=monthly_rentals["dteday"], y=monthly_rentals["count_cr"], palette="Blues", ax=ax2)
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Total Peminjaman Sepeda")
ax2.set_title("Total Peminjaman Sepeda per Bulan")
st.pyplot(fig2)

# 3. Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda Harian")
chart = alt.Chart(main_df_days).mark_line(point=True).encode(
    x='dteday:T',
    y='count_cr:Q',
    tooltip=['dteday', 'count_cr']
).interactive()
st.altair_chart(chart, use_container_width=True)

# 4. Pengaruh Cuaca terhadap Peminjaman Sepeda
st.subheader("🌦️ Pengaruh Cuaca terhadap Peminjaman Sepeda")
weather_rentals = days_df.groupby("weather_situation")["count_cr"].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.barplot(x=weather_rentals["weather_situation"], y=weather_rentals["count_cr"], palette=["#A7C7E7", "#D3D3D3", "#E57373"], ax=ax3)
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Rata-rata Penyewaan Sepeda")
ax3.set_title("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")
st.pyplot(fig3)

# 5. Pie Chart Perbandingan Pengguna
st.subheader("👥 Perbandingan Pengguna Registered vs Casual")
fig4, ax4 = plt.subplots()
labels = ['Casual', 'Registered']
sizes = [total_casual, total_registered]
ax4.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#90CAF9"], shadow=True, startangle=90)
ax4.axis('equal')
st.pyplot(fig4)

st.markdown("---")
st.markdown("📊 **Kesimpulan**")
st.write("""
1. **Peningkatan Peminjaman dari Tahun ke Tahun** 📈  
   Data menunjukkan tren positif dari 2011 ke 2012 dalam penggunaan sepeda.

2. **Musim Panas sebagai Puncak Peminjaman** ☀️  
   Jumlah peminjaman meningkat selama bulan-bulan hangat dan menurun saat musim dingin.

3. **Pengaruh Cuaca** 🌤️🌧️  
   Peminjaman lebih tinggi saat cuaca cerah dan berkurang drastis saat hujan.

4. **Penggunaan Sepeda Relatif Stabil** 📅  
   Tidak ada perbedaan signifikan antara hari kerja dan akhir pekan.

5. **Perbedaan Pengguna** 🚴‍♂️  
   Pengguna terdaftar lebih dominan dibandingkan pengguna casual.
""")
