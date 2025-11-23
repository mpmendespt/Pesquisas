// Configuração centralizada
const APP_CONFIG = {
    WORKER_URL: 'https://worker-ds.mpmendespt.workers.dev',
    BASE_URL: 'https://mpmendespt.github.io/Pesquisas',
    PATHS: {
        HOME: '/Pesquisas/index.html',
        LOGIN: '/Pesquisas/app/login.html',
        REGISTER: '/Pesquisas/app/register.html',
        DASHBOARD: '/Pesquisas/app/dashboard.html',
        ADMIN: '/Pesquisas/app/admin.html',
        PESQUISAS: '/Pesquisas/Pesquisas_/index.html'  // ✅ MANTIDO com underscore
    }
};

// Função auxiliar para obter paths
function getPath(key) {
    return APP_CONFIG.PATHS[key] || APP_CONFIG.PATHS.HOME;
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.APP_CONFIG = APP_CONFIG;
    window.getPath = getPath;
}
