(function () {
  "use strict";

  // Recover even when a thumbnail failed before this deferred script started.
  document.querySelectorAll("img[data-fallback-src]").forEach(function (thumbnail) {
    var retried = false;
    function useOriginal() {
      if (retried) return;
      retried = true;
      thumbnail.removeAttribute("srcset");
      thumbnail.removeAttribute("sizes");
      thumbnail.src = thumbnail.dataset.fallbackSrc;
    }
    thumbnail.addEventListener("error", useOriginal);
    if (thumbnail.complete && thumbnail.naturalWidth === 0) useOriginal();
  });

  var allItems = Array.from(document.querySelectorAll(".gallery-item"));
  var items = allItems;
  var lightbox = document.getElementById("gallery-lightbox");
  if (!items.length || !lightbox) return;

  // Keep the fullscreen viewer outside animated or constrained page containers.
  document.body.appendChild(lightbox);

  var image = document.getElementById("lightbox-image");
  var closeButton = lightbox.querySelector(".lightbox-close");
  var previousButton = lightbox.querySelector(".lightbox-prev");
  var nextButton = lightbox.querySelector(".lightbox-next");
  var currentIndex = 0;
  var lastTrigger = null;
  var defaultLabel = lightbox.getAttribute("aria-label");
  var touchStart = null;
  image.draggable = false;

  function show(index) {
    currentIndex = (index + items.length) % items.length;
    var item = items[currentIndex];
    var thumbnail = item.querySelector("img");
    image.src = item.dataset.full;
    image.alt = thumbnail ? thumbnail.alt : "";
    document.getElementById("lightbox-count").textContent = lightbox.dataset.counter
      .replace("{current}", String(currentIndex + 1)).replace("{total}", String(items.length));
    previousButton.hidden = items.length < 2;
    nextButton.hidden = items.length < 2;
  }

  function open(item, trigger, category) {
    var group = item.closest("[data-gallery-group]");
    items = allItems.filter(function (candidate) {
      return candidate.closest("[data-gallery-group]") === group &&
        (!category || candidate.dataset.category === category);
    });
    lightbox.setAttribute("aria-label", group ? group.dataset.galleryName : defaultLabel);
    lastTrigger = trigger;
    show(items.indexOf(item));
    lightbox.hidden = false;
    document.body.classList.add("lightbox-open");
    closeButton.focus();
  }

  function close() {
    lightbox.hidden = true;
    image.src = "";
    document.body.classList.remove("lightbox-open");
    touchStart = null;
    if (lastTrigger) lastTrigger.focus();
  }

  allItems.forEach(function (item) {
    if (item.dataset.galleryOpen) return;
    item.addEventListener("click", function () { open(item, item); });
  });

  document.querySelectorAll("[data-gallery-open]").forEach(function (button) {
    button.addEventListener("click", function () {
      var first = allItems.find(function (item) {
        var group = item.closest("[data-gallery-group]");
        return group && group.dataset.galleryGroup === button.dataset.galleryOpen &&
          (!button.dataset.galleryCategory || item.dataset.category === button.dataset.galleryCategory);
      });
      if (first) open(first, button, button.dataset.galleryCategory);
    });
  });

  closeButton.addEventListener("click", close);
  previousButton.addEventListener("click", function () { show(currentIndex - 1); });
  nextButton.addEventListener("click", function () { show(currentIndex + 1); });

  image.addEventListener("touchstart", function (event) {
    touchStart = event.touches.length === 1
      ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
  }, {passive: true});
  image.addEventListener("touchend", function (event) {
    if (!touchStart || !event.changedTouches.length || lightbox.hidden) return;
    var dx = event.changedTouches[0].clientX - touchStart.x;
    var dy = event.changedTouches[0].clientY - touchStart.y;
    touchStart = null;
    if (items.length > 1 && Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3) {
      show(currentIndex + (dx < 0 ? 1 : -1));
    }
  }, {passive: true});
  image.addEventListener("touchcancel", function () { touchStart = null; }, {passive: true});

  lightbox.addEventListener("click", function (event) {
    if (event.target === lightbox) close();
  });

  document.addEventListener("keydown", function (event) {
    if (lightbox.hidden) return;
    if (event.key === "Escape") close();
    if (event.key === "ArrowLeft" && items.length > 1) { event.preventDefault(); show(currentIndex - 1); }
    if (event.key === "ArrowRight" && items.length > 1) { event.preventDefault(); show(currentIndex + 1); }
    if (event.key === "Tab") {
      var controls = Array.from(lightbox.querySelectorAll("button:not([hidden]), a[href]"));
      var first = controls[0];
      var last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
})();
