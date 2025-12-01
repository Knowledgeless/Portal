document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("profileUpdateForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const url = "/profile/update-ajax/";

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Accept": "application/json",
            },
            body: new FormData(form)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const info = data.profile_info;
                document.getElementById("full_name").innerText = info.full_name;
                document.getElementById("email").innerText = info.email;
                document.getElementById("phone").innerText = info.phone;
                document.getElementById("dob").innerText = info.dob;
                document.getElementById("school_name").innerText = info.school_name;
                document.getElementById("student_class").innerText = info.student_class;
                document.getElementById("division").innerText = info.division;
                document.getElementById("district").innerText = info.district;
                document.getElementById("upazila").innerText = info.upazila;
                document.getElementById("gender").innerText = info.gender;

                // Hide modal
                const modalEl = document.getElementById("updateModal");
                const modal = bootstrap.Modal.getInstance(modalEl);
                modal.hide();
            } else {
                alert("Error updating profile. Check your input.");
            }
        })
        .catch(err => console.error(err));
    });
});
