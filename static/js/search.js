// search.js

// Function to load JSON data
async function loadJSON(url) {
    const response = await fetch(url);
    return response.json();
}

// Load data and colors
Promise.all([
    loadJSON('path/to/data.json'),
    loadJSON('path/to/colors.json')
]).then(([data, tagColors]) => {
    // Add event listener to the search form
    document.getElementById('searchForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const query = document.getElementById('SearchInput').value.trim();
        const results = searchItemsByTag(query, data);
        displayResults(results, query, tagColors);
    });
});

// Search function
function searchItemsByTag(query, data) {
    const matchingResults = [];

    function searchInItems(items) {
        items.forEach(item => {
            if (item.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))) {
                matchingResults.push(item);
            }
        });
    }

    // Search in projects
    Object.values(data.projects).forEach(subcategories => {
        Object.values(subcategories).forEach(items => {
            searchInItems(items);
        });
    });

    // Search in jobs
    Object.values(data.jobs.roles).forEach(items => {
        searchInItems(items);
    });

    // Search in certs
    searchInItems(data.certs);

    return matchingResults;
}

// Display function
function displayResults(results, query, tagColors) {
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = `<p>No results found for "${query}".</p>`;
        return;
    }

    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.classList.add('result-item');
        resultElement.innerHTML = `
            <h2>${result.title || result.company}</h2>
            <h3>Completion: ${result.completion || result.position}</h3>
            <p>${result.description}</p>
            <p>Tags: ${result.tags.map(tag => `<span class="tag" style="background-color: ${tagColors[tag] || '#BEE7FE'};">${tag}</span>`).join(' ')}</p>
            <a href="index.html#${result.title || result.company}">
                <button type="button" class="btn btn-outline-info">Back to Home</button>
            </a>
        `;
        resultsContainer.appendChild(resultElement);
    });
}
