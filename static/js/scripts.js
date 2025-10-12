<script>
document.getElementById('quizForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.status === 'success') {
            const tiga_terbaik = result.tiga_terbaik;

            let message = "Top 3 Rekomendasi Learning Path Kamu:\n\n";
            tiga_terbaik.forEach((item, index) => {
                message += `${index + 1}. ${item[0]} (Probabilitas: ${(item[1] * 100).toFixed(2)}%)\n`;
            });

            alert(message);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (err) {
        alert('Terjadi kesalahan: ' + err.message);
    }
});
</script>
