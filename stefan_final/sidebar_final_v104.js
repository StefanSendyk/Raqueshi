<script>
  /* VERSION 104: the sidebar watch reads 8:50 at the top of the page and 9:00 at the bottom */
  (function () {
    var t = document.getElementById('dd-time'); if (!t) return;
    function tick() { var h = document.documentElement, r = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight), m = Math.min(10, Math.floor(r * 10 + 0.0001));
      t.textContent = m >= 10 ? '9:00' : '8:5' + m; }
    tick(); addEventListener('scroll', tick, { passive: true }); addEventListener('resize', tick);
  })();
<\/script>
