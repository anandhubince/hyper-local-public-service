const searchInput = document.getElementById('searchInput');
const dateFilter = document.getElementById('dateFilter');
const categoryFilter = document.getElementById('categoryFilter');
const agentFilter = document.getElementById('agentFilter');
const newsGrid = document.getElementById('newsGrid');

let currentAudio = null;

// Populate category and agent filters
window.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.news-card');
    const categories = new Set();
    const agents = new Set();

    cards.forEach(card => {
        categories.add(card.dataset.category);
        agents.add(card.dataset.agent);
    });

    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
        categoryFilter.appendChild(option);
    });

    agents.forEach(agent => {
        const option = document.createElement('option');
        option.value = agent;
        option.textContent = agent;
        agentFilter.appendChild(option);
    });
});

// Filter news
function filterNews() {
    const keyword = searchInput.value.toLowerCase();
    const date = dateFilter.value;
    const category = categoryFilter.value.toLowerCase();
    const agent = agentFilter.value.toLowerCase();

    const cards = newsGrid.querySelectorAll('.news-card');
    cards.forEach(card => {
        const matchesKeyword = card.dataset.title.toLowerCase().includes(keyword) ||
                               card.dataset.details.toLowerCase().includes(keyword);
        const matchesDate = date ? card.dataset.date === date : true;
        const matchesCategory = category ? card.dataset.category.toLowerCase() === category : true;
        const matchesAgent = agent ? card.dataset.agent.toLowerCase() === agent : true;

        card.style.display = (matchesKeyword && matchesDate && matchesCategory && matchesAgent) ? '' : 'none';
    });
    updateHeader();
}

// Update header dynamically
function updateHeader() {
    const titleEl = document.getElementById('newsTitle');
    const taglineEl = document.getElementById('tagline');
    const dateEl = document.getElementById('editionDate');

    const selectedAgent = agentFilter.value;
    const selectedDate = dateFilter.value;

    titleEl.textContent = selectedAgent ? `News by ${selectedAgent}` : "THE DAILY CHRONICLE";
    taglineEl.textContent = selectedAgent ? `Latest stories from ${selectedAgent}` : "ALL THE NEWS THAT'S FIT TO PRINT";

    if (selectedDate) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        dateEl.textContent = new Date(selectedDate).toLocaleDateString('en-US', options);
    } else {
        dateEl.textContent = "WEDNESDAY, DECEMBER 10, 2025";
    }
}

// Clear filters
function clearFilters() {
    searchInput.value = '';
    dateFilter.value = '';
    categoryFilter.value = '';
    agentFilter.value = '';
    filterNews();
}

// Translate news
async function translateNews(newsId, lang) {
    const card = document.getElementById(`news-${newsId}`);
    const titleEl = card.querySelector('.news-title');
    const detailsEl = card.querySelector('.news-details');

    if (!lang) {
        titleEl.textContent = card.dataset.title;
        detailsEl.textContent = card.dataset.details;
        return;
    }

    try {
        const res = await fetch('/user/translate_news', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({news_id: newsId, lang: lang})
        });
        const data = await res.json();
        titleEl.textContent = data.title;
        detailsEl.textContent = data.details;
    } catch (err) {
        console.error('Translation error:', err);
    }
}

// Read news using TTS
async function readNews(newsId) {
    stopAudio();
    const card = document.getElementById(`news-${newsId}`);
    const lang = card.querySelector('select').value || 'en';

    try {
        const res = await fetch('/user/read_news', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({news_id: newsId, lang: lang})
        });
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        currentAudio = new Audio(url);
        currentAudio.play();
    } catch (err) {
        console.error("TTS error:", err);
    }
}

function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
}

// Event listeners
searchInput.addEventListener('input', filterNews);
dateFilter.addEventListener('change', filterNews);
categoryFilter.addEventListener('change', filterNews);
agentFilter.addEventListener('change', filterNews);
