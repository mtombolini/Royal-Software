$(document).ready(function() {
    // Escucha para el evento de clic en cualquier elemento con la clase "lupa-button"
    $('.lupa-button').click(function() {
        const sku = $(this).data('sku'); // Obtener el SKU desde el atributo data-sku del botón
        window.open(`/detalle/${sku}`, '_blank'); // Abrir una nueva ventana/tab con la URL "/detalle/SKU"
    });

    // Escucha para el evento de clic en cualquier elemento con la clase "respuesta-button"
    $('.respuesta-button').click(function() {
        const sku = $(this).data('sku');
        const respuesta = $(this).data('respuesta');
        
        const estaPulsado = $(this).hasClass('pulsado');

        if (estaPulsado) {
            // Si el botón ya estaba pulsado, lo desmarcamos
            $(this).removeClass('pulsado');
        } else {
            // Si el botón no estaba pulsado, primero desmarcamos todos los otros botones
            $(this).closest('tr').find('.respuesta-button').removeClass('pulsado');
            // Luego marcamos este botón como pulsado
            $(this).addClass('pulsado');
        }

        $.ajax({
            url: '/registrar_respuesta',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ sku: sku, respuesta: estaPulsado ? '' : respuesta }),
            success: function(response) {
                console.log(`Respuesta para el SKU ${sku} registrada como ${respuesta}`);
            }
        });
    });

    // Obtener las respuestas almacenadas del servidor al cargar la página
    $.ajax({
        url: '/obtener_respuestas',
        method: 'GET',
        success: function(response) {
            for (const [sku, estado] of Object.entries(response)) {
                // Encuentra el botón que corresponde a este SKU y estado, y agrégale la clase 'pulsado'
                $(`[data-sku="${sku}"][data-respuesta="${estado}"]`).addClass('pulsado');
            }
        }
    });
});
