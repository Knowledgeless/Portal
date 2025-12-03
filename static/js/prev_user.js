document.addEventListener("DOMContentLoaded", function () {
    // Initialize modal only if it exists
    const modalEl = document.getElementById("updateModal");
    if (!modalEl) return;

    let modalInstance = null;

    // Show modal only if form is displayed AND there's a query parameter (register or show_update)
    // This prevents auto-opening when user just clicks "Edit Profile" button
    const urlParams = new URLSearchParams(window.location.search);
    const hasRegisterParam = urlParams.has("register") || urlParams.has("show_update");
    const showUpdate = document.querySelector("form#registrationForm");
    
    if (showUpdate && hasRegisterParam) {
        // Use a small timeout to ensure Bootstrap JS is ready
        setTimeout(() => {
            if (!modalInstance) {
                modalInstance = new bootstrap.Modal(modalEl, { backdrop: "static", keyboard: false });
                modalInstance.show();
            }
        }, 100);
    }

    // Handle modal close - redirect to clean profile page
    modalEl.addEventListener("hidden.bs.modal", function () {
        window.location.href = window.location.pathname;
    });

    // Step navigation
    const nextStepBtn = document.getElementById("nextStep");
    const prevStepBtn = document.getElementById("prevStep");
    const step1 = document.getElementById("step-1");
    const step2 = document.getElementById("step-2");
    const progress = document.getElementById("registrationProgress");

    if (nextStepBtn) {
        nextStepBtn.onclick = function () {
            step1.style.display = "none";
            step2.style.display = "block";
            if (progress) progress.style.width = "100%";
        };
    }

    if (prevStepBtn) {
        prevStepBtn.onclick = function () {
            step2.style.display = "none";
            step1.style.display = "block";
            if (progress) progress.style.width = "50%";
        };
    }
});
