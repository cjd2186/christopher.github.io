document.addEventListener('DOMContentLoaded', () => {
    fetch('/christopher.github.io/static/about.txt')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(data => {
        console.log(data)
        // Replace new line characters with <br> tags
        const formattedData = data.replace(/(?:\r\n|\r|\n)/g, '<br>');
        // Set the formatted data as HTML content of the paragraph
        document.getElementById('about').innerHTML = formattedData;
      })
      .catch(error => {
        console.error('Error fetching the text file:', error);
      });
  });
  