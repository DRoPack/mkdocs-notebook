document.addEventListener("DOMContentLoaded", () => {
  // Select all toggle buttons
  const toggleButtons = document.querySelectorAll(".opblock-summary-control");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // Toggle the display of the associated opblock-body
      const opblockBody = button
        .closest(".opblock")
        .querySelector(".opblock-body");
      const arrow = button.querySelector(".arrow");

      opblockBody.classList.toggle("visible");
      arrow.classList.toggle("open");
    });
  });
});
