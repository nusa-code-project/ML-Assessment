from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Model Load
joblib.load('model_nusaCode.pkl')

# load question & Pilihan Ganda

soal = [
    '1. Kamu buka website dan tampilannya berantakan, loading-nya juga lama. Hal pertama yang kamu pikirin apa?',
    '2. Kalau kamu diminta bikin tombol “Login”, hal paling penting yang bakal kamu pikirin apa?',
    '3. Suatu hari data penjualan naik dua kali lipat, tapi besoknya langsung turun. Reaksi kamu apa?',
    '4. Kamu kerja bareng tim dari berbagai bidang. Bagian mana yang paling kamu pengen pegang?',
    '5. Ada bug yang cuma muncul kalau user ngelakuin urutan langkah tertentu. Cara kamu nyari penyebabnya gimana?',
    '6. Antara tugas kreatif efek kecil dan tugas teknis dampak besar, mana yang kamu pilih?',
    '7. Kamu disuruh milih antara ngerapihin semua kode dari awal biar lebih bersih atau memperbaiki bug kecil yang sering muncul. Kamu bakal...',
    '8. User bilang fitur “Cari Kursus” susah dipakai. Apa langkah pertama kamu?',
    '9. Kalau kerja bareng tim, kamu lebih suka dapet tugas yang...'
    '10. Kamu lagi ngolah data dan nemu beberapa bagian kosong. Kamu bakal ngapain?',
    '11. Kamu disuruh redesign tampilan halaman kursus biar lebih menarik. Langkah pertamamu apa?',
    '12. Cara berpikirmu lebih sering kayak gini...',
    '''
     13. (Business Acumen)
    Data nunjukin 60% user batal pas mau bayar kursus. Menurut kamu langkah paling tepat pertama kali apa?
     ''',
    '''
     14. (Business Acumen)
    Fitur baru yang kamu buat bisa ningkatin engagement user, tapi biaya server-nya tinggi banget. Apa yang bakal kamu lakuin?
     ''',
    '15. Kamu paling puas kalau hasil kerja kamu...'
]

pilihan_ganda = [
    [
        " a. Pasti ada yang salah di struktur kodenya.",
        "b. Mungkin jaringan atau device aku yang lemot.",
        "c. Pengen tahu berapa banyak orang lain yang ngalamin hal yang sama.",
        " d. Desain dan alurnya emang kurang nyaman buat user."
    ],
    [
        'a. Pastikan tampilannya rapi dan bisa dipakai semua orang.',
        'b. Harus bisa jalan di semua device tanpa bug.',
        'c. Data login-nya harus aman dan terukur.',
        'd. Flow-nya jangan bikin user bingung pas login.'
    ],
    [
        'a. Cek dulu sistem atau kodenya, takutnya error.',
        'b. Mungkin ada promo harian yang udah selesai.',
        'c. Coba analisis datanya, bisa jadi hasilnya belum akurat.',
        'd. Bisa jadi user salah paham sama promonya.'
    ],
    [
        'a. Bagian teknis dan struktur sistem.',
        'b. Bikin fitur biar bisa dipakai di berbagai perangkat.',
        'c. Analisis performa dan data hasil kerja tim.',
        'd. Mengatur alur produk biar sesuai kebutuhan user dan bisnis'
    ],
    [
        'a. Lacak satu-satu urutan fungsi yang jalan.',
        'b. Coba langsung di beberapa device.',
        'c. Analisis log atau data aktivitas user.',
        'd. Uji pengalaman user buat tahu di langkah mana mereka kesulitan'
    ],
    [
        'a. Yang teknis dulu, biar langsung keliatan hasilnya.',
        'b. Yang kreatif, soalnya lebih seru dan fleksibel.',
        'c. Lihat mana yang paling efisien dari waktu dan hasil.',
        'd. Pilih yang paling ngaruh ke user dan tujuan bisnis'
    ],
    [
        'a. Rapihin semua kode biar jangka panjangnya aman.',
        'b. Fokus ke bug kecil dulu biar sistem tetap stabil.',
        'c. Cek data error buat tahu mana yang paling sering muncul.',
        'd. Lihat bug mana yang paling ganggu user dulu baru perbaiki.'
    ],
    [
        'a. Cek dulu kodenya, mungkin logikanya belum optimal.',
        'b. Tes tampilan di HP dan laptop, siapa tahu tampilannya beda.',
        'c. Analisis data pencarian buat tahu bagian mana yang sering gagal.',
        'd. Lakukan uji coba langsung sama user buat tahu bagian mana yang bikin bingung.',
    ],
    [
        'a. Butuh logika dan struktur yang jelas.',
        'b. Bisa langsung dicoba dan dilihat hasilnya.',
        'c. Perlu analisis angka dan data buat ambil keputusan.',
        'd. Melibatkan ide, strategi, dan diskusi bareng orang lain.'
    ],
    [
        ' a. Tambah validasi biar data kosong nggak kejadian lagi.',
        ' b. Coba isi pakai data serupa yang udah ada.',
        'c. Analisis dulu kenapa bisa kosong, baru putusin mau hapus atau isi.',
        'd. Tanya tim produk apakah data kosong itu ngaruh ke keputusan user.'
    ],
    [
        'a. Cari referensi desain lain buat dapet ide layout.',
        'b. Tes tampilan di berbagai ukuran layar biar responsif.',
        'c. Analisis bagian mana yang paling sering di-skip sama user.',
        'd. Tanya user langsung bagian mana yang menurut mereka bikin ribet.'
    ],
    [
        ' a. “Gimana caranya biar sistem ini jalan cepat dan efisien?”',
        ' b. “Gimana biar hasilnya bisa dipakai di semua perangkat?”',
        'c. “Apa insight yang bisa aku ambil dari data ini?”',
        ' d. “Apakah fitur ini bener-bener penting buat user dan bisnis?”'
    ],
    [
        'a. Optimasi kecepatan halaman biar nggak lemot.',
        'b. Tes tampilan di mobile, mungkin tombol bayarnya tidak terlihat',
        'c. Cek data alur pembayaran buat tahu di step mana mereka berhenti.',
        'd. Riset alasan user batal bayar dan hitung kerugian bisnisnya.'
    ],
    [
        ' a. Tetap jalanin, yang penting fiturnya keren.',
        'b. Cari solusi teknis biar biaya server bisa ditekan.',
        'c. Hitung dulu perbandingan cost dan manfaatnya buat bisnis.',
        'd. Tanya user apakah fitur ini beneran mereka butuhin.'
    ],
    [
        'a. Berfungsi lancar tanpa error',
        'b. Bisa dipakai di mana aja dengan performa bagus.',
        'c. Ngasih insight yang bisa bantu ambil keputusan.',
        'd. Dipakai banyak orang dan bener-bener ngebantu mereka.'
    ]
]

score_mapping = {
    'a' : 1.25,
    'b' : 1.5,
    'c' : 1.75,
    'd' : 1.00
}

# Jawaban user
user_ans = []
for i, s in enumerate(soal):
    print(s)
    for opt in pilihan_ganda[i]:
        print(opt)
    while True:
        ans = input("Pilih Jawaban anda (a/b/c/d) ").lower()