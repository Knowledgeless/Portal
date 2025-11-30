document.body.classList.add("modal-open");

// step navigation
document.getElementById("nextStep").onclick = function () {
    document.getElementById("step-1").style.display = "none";
    document.getElementById("step-2").style.display = "block";
    document.getElementById("registrationProgress").style.width = "100%";
};

document.getElementById("prevStep").onclick = function () {
    document.getElementById("step-2").style.display = "none";
    document.getElementById("step-1").style.display = "block";
    document.getElementById("registrationProgress").style.width = "50%";
};