document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cropForm');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const recommendedCrop = document.getElementById('recommendedCrop');
    const confidence = document.getElementById('confidence');
    const status = document.getElementById('status');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Show loading
        loading.classList.remove('hidden');
        result.classList.add('hidden');

        // Get form data
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = parseFloat(value);
        }

        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const prediction = await response.json();

            // Hide loading
            loading.classList.add('hidden');

            if (prediction.success) {
                // Show results
                recommendedCrop.textContent = `🌾 Recommended Crop: ${prediction.crop}`;
                confidence.textContent = `🎯 Confidence: ${prediction.confidence.toFixed(1)}%`;
                
                // Set status based on confidence
                let statusText, statusClass;
                if (prediction.confidence >= 80) {
                    statusText = '✅ High Confidence';
                    statusClass = 'high';
                } else if (prediction.confidence >= 60) {
                    statusText = '⚠️ Medium Confidence';
                    statusClass = 'medium';
                } else {
                    statusText = '❌ Low Confidence';
                    statusClass = 'low';
                }
                
                status.textContent = statusText;
                status.className = `status ${statusClass}`;
                
                result.classList.remove('hidden');
            } else {
                // Show error
                recommendedCrop.textContent = '❌ Error in prediction';
                confidence.textContent = prediction.error || 'Unknown error occurred';
                status.textContent = 'Please try again';
                status.className = 'status low';
                result.classList.remove('hidden');
            }

        } catch (error) {
            // Hide loading and show error
            loading.classList.add('hidden');
            recommendedCrop.textContent = '❌ Network Error';
            confidence.textContent = 'Please check your connection and try again';
            status.textContent = 'Connection Failed';
            status.className = 'status low';
            result.classList.remove('hidden');
        }
    });

    // Add input validation
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            
            if (value < min || value > max) {
                this.style.borderColor = '#f44336';
            } else {
                this.style.borderColor = '#4CAF50';
            }
        });
    });
});
