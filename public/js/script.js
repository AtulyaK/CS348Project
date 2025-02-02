document.getElementById('fetch-data-btn').addEventListener('click', async () => {
    const response = await fetch('/api/data');
    const data = await response.json();
    document.getElementById('data-container').innerHTML = JSON.stringify(data);
  });
  