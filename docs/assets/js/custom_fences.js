document$.subscribe(function () {
  // Select all toggle buttons
  const toggleButtons = document.querySelectorAll(".opblock-summary-control");

  toggleButtons.forEach((button) => {
    // Prevent adding multiple event listeners if this runs again
    if (!button.dataset.listenerAdded) {
      button.addEventListener("click", () => {
        // Toggle the display of the associated opblock-body
        const opblockBody = button.closest(".opblock")?.querySelector(".opblock-body");
        const arrow = button.querySelector(".arrow");

        if (opblockBody) opblockBody.classList.toggle("visible");
        if (arrow) arrow.classList.toggle("open");
      });

      // Mark this button so we don’t attach multiple listeners
      button.dataset.listenerAdded = "true";
    }
  });
});
