// Select fields
const divisionSelect = document.getElementById("divisionSelect");
const districtSelect = document.getElementById("districtSelect");
const upazilaSelect = document.getElementById("upazilaSelect");

// Load Districts when division changes
divisionSelect.addEventListener("change", () => {
    const division = divisionSelect.value;

    fetch(`/api/divisions/?division=${division}`);
    fetch(`/api/districts/?division=${encodeURIComponent(division)}`)
        .then(res => res.json())
        .then(data => {
            districtSelect.innerHTML = `<option value="">-- Select District --</option>`;
            upazilaSelect.innerHTML = `<option value="">-- Select Upazila --</option>`;

            data.districts.forEach(d => {
                districtSelect.innerHTML += `<option value="${d}">${d}</option>`;
            });
        });
});

// Load Upazilas when district changes
districtSelect.addEventListener("change", () => {
    const division = divisionSelect.value;
    const district = districtSelect.value;

    fetch(`/api/upazilas/?division=${encodeURIComponent(division)}&district=${encodeURIComponent(district)}`)
        .then(res => res.json())
        .then(data => {
            upazilaSelect.innerHTML = `<option value="">-- Select Upazila --</option>`;

            data.upazilas.forEach(u => {
                upazilaSelect.innerHTML += `<option value="${u}">${u}</option>`;
            });
        });
});


window.onload = () => {
    fetch(`/api/divisions/`)
        .then(res => res.json())
        .then(data => {
            data.divisions.forEach(d => {
                divisionSelect.innerHTML += `<option value="${d}">${d}</option>`;
            });
        });
};
