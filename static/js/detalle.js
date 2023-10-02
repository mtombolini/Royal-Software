$(document).ready(function() {
    // Hacer una llamada AJAX para obtener información del producto
    $.get(`/informacion_detallada/${sku}`)
    .done(function(data) {
        let contenidoProducto = ""; 

        // Procesar la información del producto
        if (Array.isArray(data.info_producto)) {
            contenidoProducto += "Nombre del producto: " + data.info_producto[0] + "<br>";
            contenidoProducto += "SKU: " + data.info_producto[1] + "<br>";
            contenidoProducto += "Tipo: " + data.info_producto[2] + "<br>";
            contenidoProducto += "Stock: " + data.info_producto[3] + "<br>";
        } else {
            contenidoProducto += data.info_producto; // En caso de que no sea una lista, mostrar el contenido directamente.
        }

        $(".contenido-informacion").append("<p>" + contenidoProducto + "</p>");
        $(".informacion-container").append("<p>Información Estadística: " + data.info_estadistica + "</p>");
    })
    .fail(function() {
        console.log("Error al cargar la información del producto.");
    });

    $('.boton-icono').on('click', function() {
        const id = $(this).data('id');

        $('.boton-icono').removeClass('activo');
        $(this).addClass('activo');

        if (id === 'izquierdo') {
            $('.boton-icono').hide(); 
            $('.input-decision').show();
            $('.boton-cancelar').show(); 
        } else {
            $('.boton-icono').show();
            $('.input-decision').hide();
            $('.boton-cancelar').hide(); 
        }
    });

    // Al hacer clic en "Aceptar", validamos el input y cambiamos la vista
    $('.input-decision > button').on('click', function() {
        const inputValue = $('.input-decision > input').val();
        if(/^\d+$/.test(inputValue)) {  // Validamos si es un número natural
            $('.boton-icono').show();
            $('.input-decision').hide();
            $('.boton-icono[data-id="izquierdo"]').addClass('activo');
        }
    });

    // Al hacer clic en "Cancelar", se restablecen los botones
    $('.boton-cancelar').on('click', function() {
        $('.boton-icono').removeClass('activo');
        $('.boton-icono').show();
        $('.input-decision').hide();
        $(this).hide();
    });
});


