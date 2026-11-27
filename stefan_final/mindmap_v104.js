<script>
  /* VERSION 104: mind maps — one wire per card with a dot at each end; hovering a card lights its own wire */
  document.querySelectorAll('.fp-mind2').forEach(function (box) {
    var svg = box.querySelector('.mm-wires'), hub = box.querySelector('.mm-hub'), cards = [].slice.call(box.querySelectorAll('.mm-card'));
    cards.forEach(function (c, i) {
      c.setAttribute('data-n', (i < 9 ? '0' : '') + (i + 1));
      c.addEventListener('mouseenter', function () { box.classList.add('focus'); c.classList.add('hot'); var g = svg.querySelector('[data-i="' + i + '"]'); if (g) g.classList.add('hot'); });
      c.addEventListener('mouseleave', function () { box.classList.remove('focus'); c.classList.remove('hot'); [].forEach.call(svg.querySelectorAll('.hot'), function (g) { g.classList.remove('hot'); }); });
    });
    function draw() {
      var b = box.getBoundingClientRect(), h = hub.getBoundingClientRect();
      var hx = h.left + h.width / 2 - b.left, hy = h.top + h.height / 2 - b.top, r = h.width / 2 + 10, out = '';
      cards.forEach(function (c, i) {
        var q = c.getBoundingClientRect(), left = c.classList.contains('l');
        var x = (left ? q.right : q.left) - b.left, y = q.top + q.height / 2 - b.top;
        var a = Math.atan2(y - hy, x - hx), sx = hx + Math.cos(a) * r, sy = hy + Math.sin(a) * r, mx = (sx + x) / 2;
        var d = 'M' + sx + ',' + sy + ' C' + mx + ',' + sy + ' ' + mx + ',' + y + ' ' + x + ',' + y;
        out += '<g data-i="' + i + '"' + (c.classList.contains('hot') ? ' class="hot"' : '') + '><path class="w-base" d="' + d + '"/><path class="w-flow" d="' + d + '"/>' +
          '<circle class="w-dot" cx="' + sx + '" cy="' + sy + '" r="3"/><circle class="w-end" cx="' + x + '" cy="' + y + '" r="4.5"/></g>';
      });
      svg.innerHTML = out;
    }
    draw(); addEventListener('resize', draw); addEventListener('load', draw);
    if (window.ResizeObserver) new ResizeObserver(draw).observe(box);
  });
<\/script>
