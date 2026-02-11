document$.subscribe(function () {
  const sectionHeaders = document.querySelectorAll(".md-nav__link--collapsible");

  sectionHeaders.forEach((header) => {
    if (!header.dataset.listenerAdded) {
      header.addEventListener("click", function () {
        this.parentNode.classList.toggle("expanded");
      });

      header.dataset.listenerAdded = "true";
    }
  });
});
