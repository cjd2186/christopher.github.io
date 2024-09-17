document.addEventListener('DOMContentLoaded', () => {
  fetch('/static/about.txt')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(data => {
      const formattedData = data.replace(/(?:\r\n|\r|\n)/g, '<br>');
      document.getElementById('about').innerHTML = formattedData;
    })
    .catch(error => {
      console.error('Error fetching the text file:', error);
    });
});

// Function to determine font size based on tag frequency
const getFontSize = (count, maxCount) => {
const minFontSize = 14;
const maxFontSize = 36;
return ((count / maxCount) * (maxFontSize - minFontSize)) + minFontSize;
};

// Function to darken a color
const darkenColor = (color, amount) => {
  const usePound = color[0] === "#";
  const num = parseInt(color.slice(1), 16);
  let r = (num >> 16) + amount;
  let g = ((num >> 8) & 0x00FF) + amount;
  let b = (num & 0x0000FF) + amount;
  if (r > 255) r = 255;
  else if (r < 0) r = 0;
  if (g > 255) g = 255;
  else if (g < 0) g = 0;
  if (b > 255) b = 255;
  else if (b < 0) b = 0;
  return (usePound ? "#" : "") + (r << 16 | g << 8 | b).toString(16).padStart(6, '0');
};

fetch('/static/json/tags.json')
  .then(response => response.json())
  .then(tags => {
      fetch('/static/json/categories.json')
          .then(response => response.json())
          .then(categoriesData => {
              const tagCloudContainer = document.getElementById('tag-cloud');
              const maxCount = Math.max(...Object.values(tags));
              const categories = categoriesData.categories;

              // Loop through each category
              for (const [category, data] of Object.entries(categories)) {
                  const categoryContainer = document.createElement('div');
                  categoryContainer.className = 'category';
                  const categoryHeader = document.createElement('h5');
                  categoryHeader.className= 'category-title underline bold'
                  categoryHeader.textContent = category;
                  categoryContainer.appendChild(categoryHeader);

                  // Generate the tags for each category
                  for (const tag of data.tags) {
                      if (tags[tag] !== undefined) {
                          const count = tags[tag];
                          const tagElement = document.createElement('span');
                          tagElement.className = 'tag';
                          tagElement.textContent = tag;
                          tagElement.style.fontSize = `${getFontSize(count, maxCount)}px`;
                          tagElement.style.backgroundColor = data.color;

                          tagElement.addEventListener('click', () => {
                              tagElement.classList.toggle('selected');
                              if (tagElement.classList.contains('selected')) {
                                  tagElement.style.backgroundColor = darkenColor(data.color, -20);
                                  tagElement.style.fontSize = `${parseFloat(tagElement.style.fontSize) * 1.1}px`;
                              } else {
                                  tagElement.style.backgroundColor = data.color;
                                  tagElement.style.fontSize = `${parseFloat(tagElement.style.fontSize) / 1.1}px`;
                              }
                              filterProjects();
                          });

                          categoryContainer.appendChild(tagElement);
                      }
                  }
                  tagCloudContainer.appendChild(categoryContainer);
              }
          })
          .catch(error => console.error('Error fetching the categories:', error));
  })
  .catch(error => console.error('Error fetching the tags:', error));

// Function to filter projects based on selected tags
const filterProjects = () => {
  const selectedTags = Array.from(document.querySelectorAll('.tag.selected')).map(tag => tag.textContent);
  const projects = document.querySelectorAll('.project');
  const sections = document.getElementsByTagName('section');
  const sectionsArr = Array.from(sections);

  if (selectedTags.length === 0) {
      projects.forEach(project => project.style.display = 'block');
      sectionsArr.forEach(section => section.style.display = 'block');
      return;
  }

  projects.forEach(project => {
      const projectTags = project.getAttribute('data-tags').split(',');
      if (selectedTags.every(tag => projectTags.includes(tag))) {
          project.style.display = 'block';
      } else {
          project.style.display = 'none';
      }
  });

  sectionsArr.forEach(section =>{
    if (section.id === 'home' || section.id === 'contact') {
      section.style.display = 'block';
    } 
    else{
      const secproj= section.querySelectorAll('.project');
      const allProjectsHidden = Array.from(secproj).every(project => project.style.display === 'none');
      if (allProjectsHidden) {
        section.style.display = 'none';
      }   else {
        section.style.display = 'block';
      }
    }
  });
};

$(document).ready(function() {
function clearFilters() {
  const $selectedTags = $('.tag.selected');
  $selectedTags.each(function() {
    const $tagElement = $(this);
    $tagElement.removeClass('selected');
    $tagElement.css({
      'background-color': $tagElement.data('originalColor'),
      'font-size': `${getFontSize($tagElement.data('count'), maxCount)}px`
    });
  });
  filterProjects();
}

$('#reset').on('click', clearFilters);
});
