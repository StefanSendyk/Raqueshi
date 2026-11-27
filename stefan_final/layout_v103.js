<script>
  /* VERSION 103: full-width pieces need the column's position; the sidebar steps aside while one is on screen */
  (function () {
    var root = document.documentElement, main = document.querySelector('.body > main'); if (!main) return;
    function measure() { root.style.setProperty('--ml', main.getBoundingClientRect().left + 'px'); root.style.setProperty('--vw', root.clientWidth + 'px'); }
    measure(); addEventListener('resize', measure); addEventListener('load', measure);
    if (!window.IntersectionObserver) return;
    var on = new Set();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) on.add(e.target); else on.delete(e.target); });
      root.classList.toggle('side-away', on.size > 0 && innerWidth >= 1000);
    }, { rootMargin: '-25% 0px -25% 0px' });
    document.querySelectorAll('.fullw, .ch-band').forEach(function (el) { io.observe(el); });
  })();
<\/script>
