// API configuration
const API_BASE_URL = 'https://abc123.ngrok.io'; // Replace with your actual ngrok URL

// DOM elements
const modelSelect = document.getElementById('model');
const textInput = document.getElementById('text');
const generateButton = document.getElementById('generate');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const resultElement = document.getElementById('result');
const embeddingElement = document.getElementById('embedding');

// Event listeners
generateButton.addEventListener('click', generateEmbedding);

async function generateEmbedding() {
    const text = textInput.value.trim();
    const model = modelSelect.value;

    if (!text) {
        showError('Please enter some text');
        return;
    }

    // Show loading state
    showLoading();
    hideError();
    hideResult();

    try {
        const response = await fetch(`${API_BASE_URL}/embed`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                model
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate embedding');
        }

        const data = await response.json();
        showResult(data.embedding);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

function showLoading() {
    loadingElement.classList.remove('hidden');
    generateButton.disabled = true;
}

function hideLoading() {
    loadingElement.classList.add('hidden');
    generateButton.disabled = false;
}

function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
}

function hideError() {
    errorElement.classList.add('hidden');
}

function showResult(embedding) {
    embeddingElement.textContent = JSON.stringify(embedding, null, 2);
    resultElement.classList.remove('hidden');
}

function hideResult() {
    resultElement.classList.add('hidden');
} 