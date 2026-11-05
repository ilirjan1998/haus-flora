(function () {
  "use strict";
  var dialog = document.getElementById("amenities-dialog");
  var trigger = document.querySelector(".amenities-show-all");
  if (!dialog || !trigger) return;
  var scrollPosition = 0;
  trigger.addEventListener("click", function () {
    if (dialog.open) return;
    scrollPosition = window.scrollY;
    dialog.showModal();
    document.body.classList.add("amenities-open");
    dialog.querySelector(".amenities-dialog-body").scrollTop = 0;
  });
  dialog.querySelector(".amenities-close").addEventListener("click", function () { dialog.close(); });
  var backdropPointer = false;
  function outside(event) {
    var rect = dialog.getBoundingClientRect();
    return event.clientX < rect.left || event.clientX > rect.right ||
      event.clientY < rect.top || event.clientY > rect.bottom;
  }
  dialog.addEventListener("pointerdown", function (event) { backdropPointer = event.target === dialog && outside(event); });
  dialog.addEventListener("click", function (event) {
    if (backdropPointer && event.target === dialog && outside(event)) dialog.close();
    backdropPointer = false;
  });
  dialog.addEventListener("close", function () {
    document.body.classList.remove("amenities-open");
    trigger.focus({preventScroll: true});
    window.scrollTo({top: scrollPosition, behavior: "instant"});
  });
})();
