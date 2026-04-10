document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('faqSearch');
  const categoryBtns = document.querySelectorAll('.category-tab');
  const faqItems = document.querySelectorAll('.faq-item');
  const noResultsDiv = document.getElementById('noResults');
  let activeCategory = 'all';

  function filterFAQs() {
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    let visibleCount = 0;

    faqItems.forEach(item => {
      const category = item.getAttribute('data-category');
      const questionText = item.querySelector('h3')?.innerText.toLowerCase() || '';
      const answerText = item.querySelector('p')?.innerText.toLowerCase() || '';
      const text = questionText + ' ' + answerText;
      const matchesCategory = activeCategory === 'all' || category === activeCategory;
      const matchesSearch = searchTerm === '' || text.includes(searchTerm);
      
      if (matchesCategory && matchesSearch) {
        item.style.display = '';
        visibleCount++;
      } else {
        item.style.display = 'none';
      }
    });

    if (noResultsDiv) {
      noResultsDiv.classList.toggle('hidden', visibleCount > 0);
    }
  }

  // Search event
  if (searchInput) {
    searchInput.addEventListener('input', filterFAQs);
  }

  // Category tabs
  categoryBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      activeCategory = btn.innerText.toLowerCase();
      categoryBtns.forEach(b => {
        b.classList.remove('active', 'bg-primary', 'text-white');
        b.classList.add('bg-gray-100', 'text-gray-700');
      });
      btn.classList.add('active', 'bg-primary', 'text-white');
      btn.classList.remove('bg-gray-100', 'text-gray-700');
      filterFAQs();
    });
  });
});
