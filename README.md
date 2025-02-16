# Network Speed Line Chart with Bokeh

## Deskripsi Proyek
Proyek ini adalah aplikasi Python yang menggunakan Bokeh untuk membuat line chart kecepatan jaringan. Data kecepatan jaringan dapat diperoleh dari hasil pengukuran menggunakan pustaka seperti `speedtest` atau sumber lain yang relevan.

## Instalasi
Pastikan Anda memiliki Python 3.x terinstal. Kemudian, install dependensi yang diperlukan dengan perintah berikut:

```sh
pip install bokeh pandas
```

## Cara Menggunakan
1. Jalankan skrip dengan perintah:
   ```sh
   bokeh serve --show app.py
   ```
2. Aplikasi akan terbuka di browser dan menampilkan grafik kecepatan jaringan.

## Struktur Proyek
```
line-chart-bokeh/
│-- line_chart.py  # Skrip utama
│-- .venv  # Daftar dependensi
│-- README.md  # Dokumentasi proyek
```

## Contoh Kode
Berikut adalah cuplikan kode utama:

```python
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from threading import Thread
import time
import speedtest
import pandas as pd

source = ColumnDataSource(data={'time': [], 'download': [], 'upload': []})
p = figure(title='Network Speed', x_axis_label='Time', y_axis_label='Speed (Mbps)', x_axis_type='datetime')
p.line('time', 'download', source=source, line_width=2, color='blue', legend_label='Download')
p.line('time', 'upload', source=source, line_width=2, color='red', legend_label='Upload')

def update_data():
    while True:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e6  # Convert to Mbps
        upload_speed = st.upload() / 1e6  # Convert to Mbps
        new_data = {'time': [pd.Timestamp.now()], 'download': [download_speed], 'upload': [upload_speed]}
        source.stream(new_data, rollover=50)
        time.sleep(10)  # Update setiap 10 detik

thread = Thread(target=update_data, daemon=True)
thread.start()
curdoc().add_root(p)
curdoc().title = 'Network Speed Monitor'
```


---
Dibuat dengan ❤️ menggunakan Bokeh.

