(function () {
  "use strict";

  var items = Array.from(document.querySelectorAll(".gallery-item"));
  var lightbox = document.getElementById("gallery-lightbox");
  if (!items.length || !lightbox) return;

  var image = document.getElementById("lightbox-image");
  var caption = document.getElementById("lightbox-caption");
  var closeButton = lightbox.querySelector(".lightbox-close");
  var previousButton = lightbox.querySelector(".lightbox-prev");
  var nextButton = lightbox.querySelector(".lightbox-next");
  var currentIndex = 0;
  var lastTrigger = null;

  function show(index) {
    currentIndex = (index + items.length) % items.length;
    var item = items[currentIndex];
    var thumbnail = item.querySelector("img");
    image.src = item.dataset.full;
    image.alt = thumbnail ? thumbnail.alt : "";
    caption.textContent = item.dataset.caption || "";
    caption.hidden = !caption.textContent;
    previousButton.hidden = items.length < 2;
    nextButton.hidden = items.length < 2;
  }

  function open(index, trigger) {
    lastTrigger = trigger;
    show(index);
    lightbox.hidden = false;
    document.body.classList.add("lightbox-open");
    closeButton.focus();
  }

  function close() {
    lightbox.hidden = true;
    image.src = "";
    document.body.classList.remove("lightbox-open");
    if (lastTrigger) lastTrigger.focus();
  }

  items.forEach(function (item, index) {
    item.addEventListener("click", function () { open(index, item); });
  });

  closeButton.addEventListener("click", close);
  previousButton.addEventListener("click", function () { show(currentIndex - 1); });
  nextButton.addEventListener("click", function () { show(currentIndex + 1); });

  lightbox.addEventListener("click", function (event) {
    if (event.target === lightbox) close();
  });

  document.addEventListener("keydown", function (event) {
    if (lightbox.hidden) return;
    if (event.key === "Escape") close();
    if (event.key === "ArrowLeft" && items.length > 1) show(currentIndex - 1);
    if (event.key === "ArrowRight" && items.length > 1) show(currentIndex + 1);
  });
})();
