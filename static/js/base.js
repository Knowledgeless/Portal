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
    
    // SIDEBAR TOGGLE + STATE
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');

    // restore previous state
    try{
        const wasCollapsed = localStorage.getItem('sidebarCollapsed');
        if (wasCollapsed === 'true') sidebar.classList.add('collapsed');
    } catch(e){ /* localStorage disabled */ }

    if(toggleBtn && sidebar){
        toggleBtn.addEventListener('click', function(){
            sidebar.classList.toggle('collapsed');
            // persist state
            try{ localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed')) } catch(e){}
        });

        // Hide the sidebar on small screens when clicking outside
        document.addEventListener('click', (e) => {
            const isSmallScreen = window.matchMedia('(max-width: 991.98px)').matches;
            if(!isSmallScreen) return;
            if(!sidebar.classList.contains('collapsed')){
                if(!sidebar.contains(e.target) && e.target !== toggleBtn && !toggleBtn.contains(e.target)){
                    sidebar.classList.add('collapsed');
                    try{ localStorage.setItem('sidebarCollapsed', 'true') } catch(e){}
                }
            }
        });
    }
});


