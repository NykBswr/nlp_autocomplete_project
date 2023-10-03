document.addEventListener('DOMContentLoaded', function () {
    const prefixInput = document.getElementById('prefix');
    const suggestionsContainer = document.getElementById('suggestions');

    prefixInput.addEventListener('input', function () {
        const prefix = prefixInput.value.trim();

        // Hanya tampilkan saran setelah pengguna mulai mengetik
        if (prefix.length === 0) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none'; // Sembunyikan kotak saran
            return;
        }

        // Send an AJAX request to your Flask app to get autocomplete suggestions
        fetch('/autocomplete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `prefix=${encodeURIComponent(prefix)}`,
            })
            .then(response => response.json())
            .then(data => {
                const suggestions = data.suggestions;
                renderSuggestions(suggestions);
            })
            .catch(error => {
                console.error('Error fetching autocomplete suggestions:', error);
            });
    });

    function renderSuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';

        if (suggestions.length === 0) {
            suggestionsContainer.style.display = 'none'; // Sembunyikan kotak saran jika tidak ada saran
            return;
        }

        suggestionsContainer.style.display = 'block'; // Tampilkan kotak saran
        suggestions.forEach((suggestion, index) => {
            const div = document.createElement('div');
            div.textContent = suggestion;

            // Tambahkan kelas jika bukan saran terakhir
            if (index < suggestions.length - 1) {
                div.classList.add('border-b');
                div.classList.add('pb-1');
            }

            div.classList.add('m-5');
            div.addEventListener('click', function () {
                // When a suggestion is clicked, update the input field with the selected suggestion
                prefixInput.value = prefixInput.value + ' ' + suggestion;
                suggestionsContainer.innerHTML = ''; // Clear suggestions
                suggestionsContainer.style.display = 'none'; // Sembunyikan kotak saran setelah memilih
            });
            suggestionsContainer.appendChild(div);
        });
    }
});