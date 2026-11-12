(() => {
    const sidebar = document.querySelector('#app-sidebar');
    const toggle = document.querySelector('[data-menu-toggle]');
    const backdrop = document.querySelector('[data-sidebar-backdrop]');

    if (sidebar && toggle && backdrop) {
        const closeSidebar = () => {
            sidebar.classList.remove('is-open');
            backdrop.classList.remove('is-visible');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-label', 'Open navigation');
        };

        toggle.addEventListener('click', () => {
            const isOpen = sidebar.classList.toggle('is-open');
            backdrop.classList.toggle('is-visible', isOpen);
            toggle.setAttribute('aria-expanded', String(isOpen));
            toggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
        });
        backdrop.addEventListener('click', closeSidebar);
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') closeSidebar();
        });
    }

    document.querySelectorAll('[data-dismiss-message]').forEach((button) => {
        button.addEventListener('click', () => button.closest('.message')?.remove());
    });
})();
