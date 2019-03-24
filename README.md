# tsunamisim
Kode simulasi tsunami menggunakan ANUGA untuk simulasi tsunami di Kabupaten Purworejo. Data sumber gempa/tsunami diadaptasi dari model yang dikembangkan Bapak Widjo Kongko, sedangkan data tinggi gelombang sumber yang dijadikan sumber simulasi di ANUGA didapatkan dari menjalankan simulasi propagasi tsunami dengan program EasyWave.

File untuk menjalankan simulasi terdiri dari 2 file:
- project.py
- scenario(....).py

Silahkan di cek versi terakhir dua file tersebut. Scenario yang saya gunakan pada saat simulasi terakhir adalah yang mengandung "composite friction" dan angka "8-0", "8-1", "8-2", "8-3", "8-5" di dalam nama file-nya karena menerapkan fungsi composite friction dengan memasukkan koefisien Manning dalam perhitungan.

File lain merupakan file input yang diperlukan untuk menjalankan simulasi.

Untuk manual teknis ANUGA yang lebih detail, silahkan <a href="https://www.researchgate.net/publication/318511561_ANUGA_User_Manual_Release_20">dibaca di sini</a>.

Untuk manual dan kode EasyWave silahkan <a href="https://gitext.gfz-potsdam.de/geoperil/easyWave">dicek di sini</a>.
