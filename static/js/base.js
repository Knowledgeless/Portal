document.addEventListener("DOMContentLoaded", function () {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();

        // Animate the progress bar
        const progress = toastEl.querySelector('.progress-bar');
        if(progress){
            progress.style.transition = "width 4s linear";
            setTimeout(() => progress.style.width = "0%", 50);
        }
    });

    // Unified sidebar toggle handler
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar') || document.querySelector('.toggle-btn');
    const arrow = toggleBtn ? toggleBtn.querySelector('.arrow') : null;

    function isSmallScreen(){
        return window.matchMedia('(max-width: 991.98px)').matches;
    }

    // Restore saved state (expanded true/false)
    try{
        if (localStorage.getItem('sidebarExpanded') === 'true') sidebar.classList.add('expanded');
    } catch(e){}

    // Set arrow rotation on load
    if (arrow && sidebar.classList.contains('expanded')) {
        arrow.style.transform = 'rotate(180deg)';
    }

    if (toggleBtn && sidebar){
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('expanded');
            try{ localStorage.setItem('sidebarExpanded', sidebar.classList.contains('expanded')) } catch(e){}
            if (arrow) arrow.style.transform = sidebar.classList.contains('expanded') ? 'rotate(180deg)' : 'rotate(0deg)';
        });

        // Close sidebar when clicking outside on small screens
        document.addEventListener('click', (e) => {
            if (!isSmallScreen()) return;
            if (!sidebar.classList.contains('expanded')) return;
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)){
                sidebar.classList.remove('expanded');
                try{ localStorage.setItem('sidebarExpanded','false') } catch(e){}
                if (arrow) arrow.style.transform = 'rotate(180deg)';
            }
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isSmallScreen() && sidebar.classList.contains('expanded')){
                sidebar.classList.remove('expanded');
                try{ localStorage.setItem('sidebarExpanded','false') } catch(e){}
                if (arrow) arrow.style.transform = 'rotate(0deg)';
            }
        });
    }

});

