document.getElementById('quizForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.top3) {
                    let message = 'Top 3 Recommended Learning Paths:\n\n';
                    result.top3.forEach((item, idx) => {
                        message += `${idx+1}. ${item.path} - ${item.prob}\n`;
                    });
                    alert(message);
                } else {
                    alert('Gagal memproses hasil Assessment.');
                }
            } catch (error) {
                console.error(error);
                alert('Terjadi kesalahan.');
            }