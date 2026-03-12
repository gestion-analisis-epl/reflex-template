import reflex as rx

RESIZE_SCRIPT = """
(function() {
    function initResizable() {
        const table = document.querySelector('table');
        if (!table) { setTimeout(initResizable, 300); return; }

        const cols = table.querySelectorAll('th');
        cols.forEach(col => {
            if (col.querySelector('.resize-handle')) return;

            col.style.position = 'relative';
            col.style.overflow = 'visible';

            const handle = document.createElement('div');
            handle.className = 'resize-handle';
            Object.assign(handle.style, {
                position: 'absolute',
                right: '0',
                top: '0',
                width: '5px',
                height: '100%',
                cursor: 'col-resize',
                userSelect: 'none',
                zIndex: '10',
            });

            handle.addEventListener('mouseenter', () => handle.style.background = 'var(--accent-8)');
            handle.addEventListener('mouseleave', () => { if (!handle._dragging) handle.style.background = 'transparent'; });

            let startX, startW;
            handle.addEventListener('mousedown', (e) => {
                handle._dragging = true;
                startX = e.pageX;
                startW = col.offsetWidth;
                handle.style.background = 'var(--accent-8)';
                e.preventDefault();
                e.stopPropagation();

                const onMove = (e) => {
                    const newW = Math.max(60, startW + (e.pageX - startX));
                    col.style.width = newW + 'px';
                    col.style.minWidth = newW + 'px';
                };
                const onUp = () => {
                    handle._dragging = false;
                    handle.style.background = 'transparent';
                    document.removeEventListener('mousemove', onMove);
                    document.removeEventListener('mouseup', onUp);
                };
                document.addEventListener('mousemove', onMove);
                document.addEventListener('mouseup', onUp);
            });

            col.appendChild(handle);
        });
    }
    initResizable();
})();
"""

def init_resizable_columns() -> rx.event.EventSpec:
    """Llama al script de columnas redimensionables via rx.call_script."""
    return rx.call_script(RESIZE_SCRIPT)