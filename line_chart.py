from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter, HoverTool
import pandas as pd
import re
from datetime import datetime

# Membaca dan memproses file
file_path = "soal_chart_bokeh.txt"

# Menyimpan data yang akan diekstrak
timestamps = []
bitrates = []

with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Mengekstrak data timestamp utama dan bitrate
current_timestamp = None
for line in lines:
    timestamp_match = re.search(r"Timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
    if timestamp_match:
        current_timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S")
        continue  # Lanjutkan ke baris berikutnya untuk mencari data bitrate
    
    bitrate_match = re.search(r"\[\s*\d+\]\s+([\d.]+)-([\d.]+)\s+sec\s+\S+\s+\S+\s+([\d.]+)\s+([KMG])bits/sec", line)
    if bitrate_match and current_timestamp:
        bitrate = float(bitrate_match.group(3))
        unit = bitrate_match.group(4)

        # Konversi ke Mbps
        if unit == "K":
            bitrate /= 1000  # Kbps ke Mbps
        elif unit == "M":
            bitrate = bitrate  # Sudah dalam Mbps
        elif unit == "G":
            bitrate *= 1000  # Gbps ke Mbps

        timestamps.append(current_timestamp)
        bitrates.append(bitrate)
        
        # Debug: Cetak baris yang cocok
        print("Matched Timestamp:", current_timestamp, "Bitrate:", bitrate)

# Menggunakan data yang diekstrak
df = pd.DataFrame({"Timestamp": timestamps, "Bitrate (Mbps)": bitrates})

# Mengelompokkan data berdasarkan timestamp yang dibulatkan ke jam terdekat
df["Timestamp"] = df["Timestamp"].dt.floor("h")  # Bulatkan ke jam terdekat
df = df.groupby("Timestamp").sum().reset_index()

print(df.head())  # Debug: Periksa hasil ekstraksi data

# Output ke file HTML
output_file("network_speed.html")

# Membuat figure
p = figure(x_axis_type="datetime", title="Testing Jaringan", width=800, height=400)
p.title.text_font_size = '20pt'
p.line(df['Timestamp'], df['Bitrate (Mbps)'], line_width=2)
p.xaxis.axis_label = "DATE TIME"
p.yaxis.axis_label = "Speed (Mbps)"

p.xaxis.formatter = DatetimeTickFormatter(
    hours="%m/%d/%Y\n%H:%M:%S",
    days="%m/%d/%Y\n%H:%M:%S",
    months="%m/%Y\n%H:%M:%S",
    years="%m/%Y\n%H:%M:%S"
)

# Menambahkan HoverTool
hover = HoverTool(
    tooltips=[
        ("Date Time", "@x{%F %H:%M:%S}"),
        ("Speed (Mbps)", "@y{0.00}")
    ],
    formatters={"@x": "datetime"},
    mode="vline"
)
p.add_tools(hover)

# Menampilkan plot
show(p)