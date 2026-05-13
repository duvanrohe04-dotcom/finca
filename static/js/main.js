// Tab switching
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    if (typeof event !== 'undefined' && event && event.target) {
        event.target.classList.add('active');
    }
}

// Auto dismiss alerts after 4s
document.addEventListener('DOMContentLoaded', () => {
    // PWA: registrar Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(() => { /* noop */ });
    }

    // PWA: botón Instalar (Android/Chrome/Edge)
    let deferredPrompt = null;
    const installButtons = Array.from(document.querySelectorAll('.pwa-install'));

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
    });

    const isIos = () => /iphone|ipad|ipod/i.test(navigator.userAgent);
    const isInStandaloneMode = () => ('standalone' in window.navigator) && window.navigator.standalone;
    const isStandaloneDisplayMode = () => window.matchMedia && window.matchMedia('(display-mode: standalone)').matches;

    // Si ya está instalada, ocultamos los botones
    if (isInStandaloneMode() || isStandaloneDisplayMode()) {
        installButtons.forEach(btn => { btn.style.display = 'none'; });
    }

    installButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            // iOS no dispara beforeinstallprompt: mostramos instrucción
            if (isIos() && !isInStandaloneMode()) {
                alert('En iPhone/iPad: toca “Compartir” y luego “Añadir a pantalla de inicio”.');
                return;
            }
            if (!deferredPrompt) {
                alert('En PC: en Chrome/Edge busca el icono de “Instalar” en la barra de direcciones o en el menú (⋮) → “Instalar Finca Admin”.');
                return;
            }
            deferredPrompt.prompt();
            await deferredPrompt.userChoice;
            deferredPrompt = null;
            installButtons.forEach(b => { b.style.display = 'none'; });
        });
    });

    // Sidebar (móvil)
    const toggleBtn = document.getElementById('sidebarToggle');
    const backdrop = document.getElementById('sidebarBackdrop');

    const openSidebar = () => document.body.classList.add('sidebar-open');
    const closeSidebar = () => document.body.classList.remove('sidebar-open');
    const toggleSidebar = () => document.body.classList.toggle('sidebar-open');

    if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);
    if (backdrop) backdrop.addEventListener('click', closeSidebar);

    // Cierra el menú al navegar (móvil)
    document.querySelectorAll('.sidebar a.nav-item').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) closeSidebar();
        });
    });

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.4s';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });
});
