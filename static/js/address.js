document.addEventListener("DOMContentLoaded", function() {
    const step1 = document.getElementById("step-1"),
          step2 = document.getElementById("step-2"),
          nextBtn = document.getElementById("nextStep"),
          prevBtn = document.getElementById("prevStep"),
          progressBar = document.getElementById("registrationProgress");

    // Step 1 inputs
    const step1Fields = Array.from(step1.querySelectorAll("input, select"));

    nextBtn.addEventListener("click", function() {
        let invalid = step1Fields.some(f => !f.value || (f.tagName==="SELECT" && f.value===""));
        if (invalid) {
            alert("Please fill all required fields in Step 1");
            return;
        }
        step1.style.display="none";
        step2.style.display="block";
        progressBar.style.width="100%";
        progressBar.setAttribute("aria-valuenow","100");
        window.scrollTo(0,0);
    });

    prevBtn.addEventListener("click", function() {
        step2.style.display="none";
        step1.style.display="block";
        progressBar.style.width="50%";
        progressBar.setAttribute("aria-valuenow","50");
        window.scrollTo(0,0);
    });

    // Cascading address
    const division = document.getElementById("id_division"),
          district = document.getElementById("id_district"),
          upazila = document.getElementById("id_upazila");
    district.disabled = true; upazila.disabled = true;

    function fetchOptions(url, select, placeholder){
        fetch(url).then(r=>r.json()).then(data=>{
            select.innerHTML=`<option value="">${placeholder}</option>`;
            Object.values(data)[0].forEach(v=>{
                const opt=document.createElement("option");
                opt.value=v; opt.textContent=v; select.appendChild(opt);
            });
            select.disabled=false;
        });
    }

    division.addEventListener("change", ()=>{ 
        if(!division.value){ district.disabled=true; upazila.disabled=true; return; }
        fetchOptions(`/api/districts/?division=${division.value}`, district, "-- Select District --");
        upazila.innerHTML=`<option value="">-- Select Upazila --</option>`; upazila.disabled=true;
    });

    district.addEventListener("change", ()=>{ 
        if(!district.value){ upazila.disabled=true; return; }
        fetchOptions(`/api/upazilas/?division=${division.value}&district=${district.value}`, upazila, "-- Select Upazila --");
    });

    // Initial load divisions
    fetchOptions(`/api/divisions/`, division, "-- Select Division --");
});
