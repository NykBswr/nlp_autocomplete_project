document.addEventListener('DOMContentLoaded', function () {
    const prefixInput = document.getElementById('prefix');
    const suggestionsContainer = document.getElementById('suggestions2');

    prefixInput.addEventListener('input', function () {
        const prefix = prefixInput.value.trim();

        // Only display suggestions after the user starts typing
        if (prefix.length === 0) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none'; // Hide the suggestions box
            return;
        }

        // Send an AJAX request to your Flask app to get BILSTM suggestions
        fetch('/autocombilstm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `prefix=${encodeURIComponent(prefix)}`,
            })
            .then(response => response.json())
            .then(data => {
                const suggestions = data.suggestions2;
                renderSuggestions(suggestions);
            })
            .catch(error => {
                console.error('Error fetching autocomplete suggestions:', error);
            });

    });

    function renderSuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';

        if (suggestions.length === 0) {
            suggestionsContainer.style.display = 'none'; // Hide the suggestions box if there are no suggestions
            return;
        }

        suggestionsContainer.style.display = 'block'; // Show the suggestions box
        suggestions.forEach((suggestion, index) => {
            const div = document.createElement('div');
            div.textContent = suggestion;

            // Add classes if it's not the last suggestion
            if (index < suggestions.length - 1) {
                div.classList.add('border-b');
                div.classList.add('pb-1');
            }

            div.classList.add('m-5');
            div.addEventListener('click', function () {
                // When a suggestion is clicked, update the input field with the selected suggestion
                prefixInput.value = prefixInput.value + suggestion;
                suggestionsContainer.innerHTML = ''; // Clear suggestions
                suggestionsContainer.style.display = 'none'; // Hide the suggestions box after selection
            });
            suggestionsContainer.appendChild(div);
        });
    }
});