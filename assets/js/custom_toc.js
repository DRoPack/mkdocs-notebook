document.addEventListener("DOMContentLoaded", function () {
  const sectionHeaders = document.querySelectorAll(
    ".md-nav__link--collapsible"
  );
  sectionHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      this.parentNode.classList.toggle("expanded");
    });
  });
});
