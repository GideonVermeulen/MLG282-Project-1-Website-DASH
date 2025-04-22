// script.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predict-form");
    const submitBtn = document.querySelector(".submit-button");
  
    form.addEventListener("submit", () => {
      // prevent double submits
      submitBtn.disabled = true;
      submitBtn.textContent = "Predicting...";
    });
  });
  