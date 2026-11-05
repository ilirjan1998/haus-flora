/* A language switch follows the current reading position, never an old anchor. */
(function () {
  'use strict';
  var link = document.querySelector('[data-preserve-hash]');
  var key = 'haus-flora-language-position';
  if (link) {
    var url = new URL(link.href, location.href);
    url.hash = '';
    link.href = url.href;
    link.addEventListener('click', function (event) {
      if (event.button || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      try { sessionStorage.setItem(key, JSON.stringify({path: url.pathname, y: window.scrollY, time: Date.now()})); } catch (_) {}
    });
  }
  var saved;
  try { saved = JSON.parse(sessionStorage.getItem(key)); sessionStorage.removeItem(key); } catch (_) {}
  if (!saved || saved.path !== location.pathname || Date.now() - saved.time > 30000 || location.hash) return;
  var active = true;
  function restore() { if (active) window.scrollTo({top: saved.y, behavior: 'instant'}); }
  restore();
  window.addEventListener('load', restore, {once: true});
  if (document.fonts) document.fonts.ready.then(restore);
  ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (event) {
    window.addEventListener(event, function () { active = false; }, {once: true, passive: true});
  });
})();

/* Keep cross-page section links aligned while images, fonts and the calendar load. */
(function () {
  'use strict';
  var main = document.getElementById('main-content');
  if (!main) return;
  var target = null;
  var frame = 0;
  var expiry = 0;
  var observer = null;

  function stop() {
    target = null;
    cancelAnimationFrame(frame);
    clearTimeout(expiry);
    if (observer) observer.disconnect();
  }
  function align() {
    frame = 0;
    if (!target) return;
    var box = target.getBoundingClientRect();
    var viewport = window.innerHeight;
    var gap = box.height > 0 && box.height < viewport - 48
      ? Math.max(24, (viewport - box.height) / 2) : 24;
    var top = Math.max(0, window.scrollY + box.top - gap);
    // Explicitly bypass global smooth scrolling during layout corrections.
    var root = document.documentElement;
    var previous = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    window.scrollTo({top: top, behavior: 'instant'});
    root.style.scrollBehavior = previous;
  }
  function schedule() {
    if (!target || frame) return;
    frame = requestAnimationFrame(align);
  }
  function begin() {
    stop();
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); }
    catch (_) { return; }
    var element = id && document.getElementById(id);
    if (!element || !main.contains(element)) return;
    target = element.classList.contains('gallery-anchor') ? element.parentElement : element;
    if (window.ResizeObserver) {
      observer = new ResizeObserver(schedule);
      observer.observe(main);
      observer.observe(target);
    }
    schedule();
    expiry = setTimeout(stop, 10000);
  }
  window.addEventListener('hashchange', begin);
  window.addEventListener('load', schedule);
  main.addEventListener('load', schedule, true);
  if (document.fonts) document.fonts.ready.then(schedule);
  ['wheel', 'touchstart', 'pointerdown'].forEach(function (event) {
    window.addEventListener(event, stop, {passive: true});
  });
  window.addEventListener('keydown', function (event) {
    if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' ', 'Tab'].indexOf(event.key) !== -1) stop();
  });
  // Re-align even when the selected section already matches the URL hash.
  document.addEventListener('click', function (event) {
    if (event.target.closest('.back-to-menu')) { stop(); return; }
    var link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank') return;
    var url = new URL(link.href, window.location.href);
    if (url.origin === window.location.origin && url.pathname === window.location.pathname && url.search === window.location.search && url.hash) {
      setTimeout(begin, 0);
    }
  });
  begin();
})();

/* Show a quiet return control only after the main menu has left the viewport. */
(function () {
  'use strict';
  var menu = document.getElementById('site-navigation');
  var button = document.querySelector('.back-to-menu');
  if (!menu || !button) return;
  function update() { button.hidden = menu.getBoundingClientRect().bottom > 0; }
  if (window.IntersectionObserver) {
    new IntersectionObserver(update).observe(menu);
  } else {
    window.addEventListener('scroll', update, {passive: true});
  }
  window.addEventListener('resize', update);
  window.addEventListener('pageshow', update);
  button.addEventListener('click', function () {
    menu.focus({preventScroll: true});
    window.scrollTo({top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  });
  update();
})();
