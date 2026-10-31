(function () {
  'use strict';

  var grid = document.getElementById('games');
  if (!grid) {
    return;
  }

  var search = document.getElementById('search');
  var sort = document.getElementById('sort');
  var count = document.getElementById('count');
  var empty = document.getElementById('empty');
  var filterButtons = document.querySelectorAll('.filters button');
  var activeFilter = 'all';
  var query = '';
  var timer;

  var items = Array.prototype.map.call(grid.children, function (el) {
    function attr(name) {
      return el.getAttribute('data-' + name) || '';
    }

    return {
      el: el,
      name: attr('name'),
      year: Number(attr('year')) || 0,
      playtime: Number(attr('playtime')) || 0,
      recent: Number(attr('recent')) || 0,
      positive: Number(attr('positive')),
      reviews: Number(attr('reviews')) || 0,
      achievements: Number(attr('achievements')),
      haystack: (attr('name') + ' ' + attr('devs')).toLowerCase()
    };
  });

  function isVisible(item) {
    if (query && item.haystack.indexOf(query) === -1) {
      return false;
    }
    if (activeFilter === 'played' && item.playtime <= 0) {
      return false;
    }
    if (activeFilter === 'unplayed' && item.playtime > 0) {
      return false;
    }
    if (activeFilter === 'recent' && item.recent <= 0) {
      return false;
    }
    return true;
  }

  function compare(a, b) {
    switch (sort.value) {
      case 'recent':
        return b.recent - a.recent || b.playtime - a.playtime;
      case 'name':
        return a.name.localeCompare(b.name);
      case 'year':
        return b.year - a.year;
      case 'positive':
        return b.positive - a.positive || b.reviews - a.reviews;
      case 'achievements':
        return b.achievements - a.achievements;
      default:
        return b.playtime - a.playtime;
    }
  }

  function render() {
    var list = items.filter(isVisible).sort(compare);
    var fragment = document.createDocumentFragment();

    list.forEach(function (item) {
      fragment.appendChild(item.el);
    });

    grid.replaceChildren(fragment);
    count.textContent =
      list.length.toLocaleString() + (list.length === 1 ? ' game' : ' games');
    empty.hidden = list.length !== 0;
  }

  search.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      query = search.value.trim().toLowerCase();
      render();
    }, 120);
  });

  sort.addEventListener('change', render);

  Array.prototype.forEach.call(filterButtons, function (button) {
    button.addEventListener('click', function () {
      activeFilter = button.getAttribute('data-filter');
      Array.prototype.forEach.call(filterButtons, function (other) {
        var isActive = other === button;
        other.classList.toggle('is-active', isActive);
        other.setAttribute('aria-pressed', String(isActive));
      });
      render();
    });
  });

  render();
})();
