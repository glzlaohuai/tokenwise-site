/* Shared: language toggle (EN default, remembered, no mixing) + scroll reveal. */
(function () {
  var doc = document.documentElement;

  function apply(l, save) {
    doc.setAttribute('data-lang', l);
    doc.setAttribute('lang', l === 'zh' ? 'zh-CN' : 'en');
    var t = doc.getAttribute(l === 'zh' ? 'data-title-zh' : 'data-title-en');
    if (t) document.title = t;
    var b = document.querySelectorAll('[data-set-lang]');
    for (var i = 0; i < b.length; i++)
      b[i].setAttribute('aria-pressed', b[i].getAttribute('data-set-lang') === l ? 'true' : 'false');
    if (save) { try { localStorage.setItem('tw-lang', l); } catch (e) {} }
  }

  var btns = document.querySelectorAll('[data-set-lang]');
  for (var i = 0; i < btns.length; i++)
    (function (x) { x.addEventListener('click', function () { apply(x.getAttribute('data-set-lang'), true); }); })(btns[i]);
  apply(doc.getAttribute('data-lang') || 'en', false);

  // reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && els.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    for (var j = 0; j < els.length; j++) io.observe(els[j]);
  } else {
    for (var k = 0; k < els.length; k++) els[k].classList.add('in');
  }
})();
