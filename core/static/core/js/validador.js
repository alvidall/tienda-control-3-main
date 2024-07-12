// alert(1);

$(document).ready(function() {

  // Agregar método de validación para RUT chileno
  $.validator.addMethod("rutChileno", function(value, element) {
    // Validar que el RUT tenga el formato correcto (8 o 9 dígitos + guión + dígito verificador)
    var rutPattern = /^\d{7,8}-[\dkK]$/;
    if (!rutPattern.test(value)) {
        return false;
    }

    // Validar el dígito verificador
    var rutSinGuion = value.replace("-", "");
    var rut = rutSinGuion.slice(0, -1);
    var dv = rutSinGuion.slice(-1).toUpperCase(); // Convertir a mayúscula para comparar con "K"
    var factor = 2;
    var sum = 0;
    for (var i = rut.length - 1; i >= 0; i--) {
        sum += parseInt(rut.charAt(i)) * factor;
        factor = factor === 7 ? 2 : factor + 1;
    }
    var dvCalculado = 11 - (sum % 11);
    if (dvCalculado === 11) {
        dvCalculado = "0";
    } else if (dvCalculado === 10) {
        dvCalculado = "K";
    } else {
        dvCalculado = dvCalculado.toString();
    }

    return dv === dvCalculado;
  }, "El RUT no es válido (escriba sin puntos y con guión)");


  // Agregar método de validación para correo
  $.validator.addMethod("emailCompleto", function(value, element) {

    // Expresión regular para validar correo electrónico
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z\-0-9]{2,}))$/;

    // Validar correo electrónico con la expresión regular
    return regex.test(value);

  }, 'El formato del correo no es válido');
  
  // Agregar método de validación para que un campo sólo acepte 
  // letras y espacios en blanco, pero no números ni símbolos,
  // ideal para campos como nombres y apellidos
  $.validator.addMethod("soloLetras", function(value, element) {

    return this.optional(element) || /^[a-zA-Z\s]*$/.test(value);

  }, "Sólo se permiten letras y espacios en blanco.");

  $("#formulario-registro").validate({
    rules: {
      rut: {
        required: true,
        rutChileno: true
      },
      nombre: {
        required: true,
        soloLetras: true
      },
      correo: {
        required: true,
        emailCompleto: true,
      },
      password: {
        required: true,
        minlength: 5,
        maxlength: 15,
      },
      password2: {
        required: true,
        minlength: 5,
        maxlength: 15,
        equalTo: "#password",
      },
    }, // --> Fin de reglas
    messages: {
      rut: {
        required: "El RUT es un campo requerido",
        rutChileno: "El RUT no es válido (escriba sin puntos y con guión)"
      },
      nombre: {
        required: "El nombre es un campo requerido",
        soloLetras: "El nombre sólo puede contener letras y espacios en blanco",
      },
      correo: {
        required: "El correo es un campo requerido",
        email: "El formato del correo no es válido",
      },
      password: {
        required: "La contraseña es un campo requerido",
        minlength: "La contraseña debe tener un mínimo de 5 caracteres",
        maxlength: "La contraseña debe tener un máximo de 15 caracteres",
      },
      password2: {
        required: "Repetir contraseña es un campo requerido",
        minlength: "Repetir contraseña debe tener un mínimo de 5 caracteres",
        maxlength: "Repetir contraseña debe tener un máximo de 15 caracteres",
        equalTo: "Debe repetir la contraseña escrita anteriormente",
      },
    }, // --> Fin de mensajes
  });
  
});
// validador.js

$(document).ready(function() {
  // Validación para el formulario de registro de productos
  $("#formulario-producto").validate({
      rules: {
          id: {
              required: true,
              digits: true
          },
          categoria: {
              required: true
          },
          nombre: {
              required: true
          },
          descripcion: {
              required: true
          },
          precio: {
              required: true,
              number: true
          },
          descuentoSubscriptor: {
              required: true,
              number: true,
              range: [0, 100]
          },
          descuentoOferta: {
              required: true,
              number: true,
              range: [0, 100]
          }
      },
      messages: {
          id: {
              required: "El ID es obligatorio",
              digits: "El ID debe ser un número entero"
          },
          categoria: {
              required: "La categoría es obligatoria"
          },
          nombre: {
              required: "El nombre del producto es obligatorio"
          },
          descripcion: {
              required: "La descripción es obligatoria"
          },
          precio: {
              required: "El precio es obligatorio",
              number: "El precio debe ser un número"
          },
          descuentoSubscriptor: {
              required: "El descuento para subscriptores es obligatorio",
              number: "El descuento debe ser un número",
              range: "El descuento debe estar entre 0 y 100"
          },
          descuentoOferta: {
              required: "El descuento por oferta es obligatorio",
              number: "El descuento debe ser un número",
              range: "El descuento debe estar entre 0 y 100"
          }
      },
      submitHandler: function(form) {
          // Acción al enviar el formulario, por ejemplo:
          alert('Producto registrado correctamente!');
          form.submit();
      }
  });
});
$(document).ready(function() {
  // Añadir reglas de validación a los campos individuales
  $("#Correo").rules("add", {
      required: true,
      email: true,
      messages: {
          required: "Por favor, ingrese su correo electrónico.",
          email: "Por favor, ingrese un correo electrónico válido."
      }
  });

  $("#password").rules("add", {
      required: true,
      minlength: 6,
      messages: {
          required: "Por favor, ingrese su contraseña.",
          minlength: "Su contraseña debe tener al menos 6 caracteres."
      }
  });

  // Manejar el evento de clic del botón de ingreso
  $(".boton_ingresar").click(function() {
      var isValid = true;
      // Validar cada campo individualmente
      if (!$("#Correo").valid()) {
          isValid = false;
      }
      if (!$("#password").valid()) {
          isValid = false;
      }

      if (isValid) {
          alert("Formulario válido y enviado!");
          // Aquí iría el código para enviar el formulario
      } else {
          alert("Por favor, complete los campos correctamente.");
      }
  });
});
// validador.js

$(document).ready(function() {
  // Agregar método de validación para números
  $.validator.addMethod("numeroValido", function(value, element) {
      return this.optional(element) || /^[0-9]+$/.test(value);
  }, "La cantidad debe ser un número válido");

  // Validación del formulario
  $("#formulario").validate({
      rules: {
          cantidad: {
              required: true,
              numeroValido: true
          }
      },
      messages: {
          cantidad: {
              required: "La cantidad es un campo requerido",
              numeroValido: "La cantidad debe ser un número válido"
          }
      },
      errorPlacement: function(error, element) {
          var name = element.attr("name");
          $("#" + name + "Error").html(error);
      },
      highlight: function(element) {
          $(element).addClass('is-invalid');
      },
      unhighlight: function(element) {
          $(element).removeClass('is-invalid');
      }
  });

  // Manejador de los botones (ejemplo de manejo del botón "Agregar")
  $('.btn-primary').click(function(event) {
      if ($("#formulario").valid()) {
          alert('Formulario validado y enviado correctamente'); // Reemplaza esto con el manejo real del formulario
      }
  });
});
