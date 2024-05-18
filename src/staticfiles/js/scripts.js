// scripts.js

document.addEventListener('DOMContentLoaded', () => {
  const toggleSearchBtn = document.querySelector('.toggle-search-btn');
  const searchBar = document.querySelector('.search-bar');

  toggleSearchBtn.addEventListener('click', () => {
      searchBar.classList.toggle('show');
  });
});
