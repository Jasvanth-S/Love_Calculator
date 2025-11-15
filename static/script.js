document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loveForm');
    const loader = document.getElementById('loader');
    const btnText = document.querySelector('.btn-text');
    const resultContainer = document.getElementById('resultContainer');
    const percentageValue = document.getElementById('percentageValue');
    const namesDisplay = document.getElementById('namesDisplay');
    const resultMessage = document.getElementById('resultMessage');
    const shareBtn = document.getElementById('shareBtn');

    // Auto-detect if running on ngrok
    if (window.location.hostname.includes('ngrok.io') || window.location.hostname.includes('ngrok-free.app')) {
        console.log('🌐 Running on ngrok! Sharing will work globally.');
        // Set the ngrok URL for backend sharing
        fetch('/set-ngrok-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: window.location.origin + '/'
            })
        });
    }

    // Love messages based on percentage ranges
    const loveMessages = {
        90: "💕 Perfect Match! You two are soulmates! 💕",
        80: "❤️ Excellent compatibility! Love is in the air! ❤️",
        70: "💖 Great potential for a beautiful relationship! 💖",
        60: "💝 Good chemistry! Give it a chance! 💝",
        50: "💛 Friendship could blossom into something more! 💛",
        40: "🤝 Better as friends, but who knows? 🤝",
        30: "😊 Not the strongest match, but miracles happen! 😊",
        20: "🤔 It might be challenging, but love conquers all! 🤔",
        10: "😅 Opposites attract sometimes! 😅",
        0: "🙃 Maybe try being friends first! 🙃"
    };

    function getLoveMessage(percentage) {
        for (let threshold of [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]) {
            if (percentage >= threshold) {
                return loveMessages[threshold];
            }
        }
        return loveMessages[0];
    }

    function animatePercentage(targetPercentage) {
        let currentPercentage = 0;
        const increment = targetPercentage / 50; // Animation duration control
        
        const animation = setInterval(() => {
            currentPercentage += increment;
            if (currentPercentage >= targetPercentage) {
                currentPercentage = targetPercentage;
                clearInterval(animation);
            }
            percentageValue.textContent = Math.round(currentPercentage);
        }, 20);
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name1 = document.getElementById('name1').value.trim();
        const name2 = document.getElementById('name2').value.trim();
        const dob1 = document.getElementById('dob1').value;
        const dob2 = document.getElementById('dob2').value;

        // Validation
        if (!name1 || !name2 || !dob1 || !dob2) {
            alert('Please fill in all fields!');
            return;
        }

        // Check if dates are not in the future
        const today = new Date().toISOString().split('T')[0];
        if (dob1 > today || dob2 > today) {
            alert('Date of birth cannot be in the future!');
            return;
        }

        // Show loading state
        loader.style.display = 'inline-block';
        btnText.textContent = 'Calculating...';
        form.querySelector('button').disabled = true;

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name1: name1,
                    name2: name2,
                    dob1: dob1,
                    dob2: dob2
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Display results
                namesDisplay.textContent = `${data.name1} ❤️ ${data.name2}`;
                resultMessage.textContent = getLoveMessage(data.percentage);
                
                // Animate percentage
                percentageValue.textContent = '0';
                animatePercentage(data.percentage);
                
                // Setup share button
                shareBtn.onclick = function() {
                    window.open(`/share/${encodeURIComponent(data.name1)}/${encodeURIComponent(data.name2)}/${data.percentage}`, '_blank');
                };
                
                // Show result container
                resultContainer.style.display = 'block';
                resultContainer.scrollIntoView({ behavior: 'smooth' });
                
            } else {
                alert(data.error || 'An error occurred while calculating love percentage.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Network error. Please check your connection and try again.');
        } finally {
            // Reset loading state
            loader.style.display = 'none';
            btnText.textContent = 'Calculate Love ❤️';
            form.querySelector('button').disabled = false;
        }
    });

    // Add input validation and formatting
    const nameInputs = document.querySelectorAll('#name1, #name2');
    nameInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Capitalize first letter
            this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
        });
    });

    // Add date validation
    const dateInputs = document.querySelectorAll('#dob1, #dob2');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.setAttribute('max', today);
    });
});

function resetForm() {
    document.getElementById('loveForm').reset();
    document.getElementById('resultContainer').style.display = 'none';
    document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
}
