document.addEventListener("DOMContentLoaded", function () {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.map(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();

        // Animate the progress bar
        const progress = toastEl.querySelector('.progress-bar');
        if(progress){
            progress.style.transition = "width 4s linear";
            setTimeout(() => progress.style.width = "0%", 50);
        }
    });
});


