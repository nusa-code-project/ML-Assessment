class QuizApp {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.init();
    }

    init() {
        if (!this.form) {
            console.error('Form not found!');
            return;
        }

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.form);

        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            this.handleResult(result);
        } catch (error) {
            console.error('Error submitting quiz:', error);
            alert('Terjadi kesalahan saat mengirim data. Silakan coba lagi.');
        }
    }

    handleResult(result) {
        if (result.status === 'error') {
            alert(result.message);
            return;
        }

        if (result.top3) {
            let message = '🎯 Top 3 Recommended Learning Paths:\n\n';
            result.top3.forEach((item, idx) => {
                message += `${idx + 1}. ${item.path} - ${item.prob}\n`;
            });
            alert(message);
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {
    new QuizApp('quizForm');
});
