import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='Hcavill',
        tipo='Cliente', 
        nombre='Henry', 
        apellido='Cavill', 
        correo=test_user_email if test_user_email else 'Hcavill@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/Henry_Cavill.webp')

    crear_usuario(
        username='Auron',
        tipo='Cliente', 
        nombre='Raúl', 
        apellido='Álvarez', 
        correo=test_user_email if test_user_email else 'auron@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/auron.jpg')

    crear_usuario(
        username='gnewell',
        tipo='Cliente', 
        nombre='Gave', 
        apellido='Newell', 
        correo=test_user_email if test_user_email else 'gnewell@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/gave newell.jpg')

    crear_usuario(
        username='Xokas',
        tipo='Cliente', 
        nombre='Joaquin', 
        apellido='Dominguez', 
        correo=test_user_email if test_user_email else 'xokas@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/xokas.jpg')

    crear_usuario(
        username='Kreeves',
        tipo='Administrador', 
        nombre='Keanu', 
        apellido='Reeves', 
        correo=test_user_email if test_user_email else 'kreeves@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/Keanu reeves.webp')
    
    crear_usuario(
        username='Rubius',
        tipo='Administrador', 
        nombre='Rubén', 
        apellido='Doblas', 
        correo=test_user_email if test_user_email else 'rubius@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/rubius.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Alejandro',
        apellido='Vidal',
        correo=test_user_email if test_user_email else 'al.vidall@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/illojuan.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Rust',
            'descripcion': 'El único objetivo en Rust es sobrevivir. Todo quiere que mueras: la fauna de la isla y otros habitantes, el entorno, otros sobrevivientes. Haz lo que sea necesario para sobrevivir otra noche.',
            'precio': 17900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/rust.jpeg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Hades II',
            'descripcion': 'Usa las artes oscuras para abrirte paso más allá del inframundo y enfréntate al Titán del Tiempo en esta cautivadora continuación del galardonado juego de mazmorras de tipo rogue-like.',
            'precio': 15500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/hades.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Call of Duty: Modern Warfare III',
            'descripcion': 'En la secuela directa del exitoso juego Call of Duty®: Modern Warfare® II, el capitán Price y la Fuerza operativa 141 se enfrentan a la amenaza definitiva.',
            'precio': 54990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/cod.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Like a Dragon: Infinite Wealth',
            'descripcion': 'Dos héroes más grandes que la vida misma se unen guiados por el destino, o quizás, por algo más siniestro… Disfruta de la vida en Japón y explora todo lo que ofrece Hawái en una aventura tan grande que abarca todo el Pacífico.',
            'precio': 60900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/likeadragon.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Middle-earth™: Shadow of War™',
            'descripcion': 'Disfruta de un mundo abierto épico, recreado por el galardonado sistema Némesis. Forja un nuevo Anillo de Poder, conquista fortalezas en grandes batallas y domina Mordor con tu propio ejército de orcos en La Tierra Media™: Sombras de Guerra™.',
            'precio': 37999,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/shadowofwar.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy es un RPG inmersivo de acción en mundo abierto. Ahora puedes tomar el control de la acción y ser el centro de tu propia aventura en el mundo mágico.',
            'precio': 39999,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/hogwarts_legacy.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Granblue Fantasy: Relink',
            'descripcion': 'Una gran aventura te aguarda en los cielos! Elige entre un variopinto plantel de navegantes para formar un grupo de cuatro y empuña tu espada, tu arma o tu magia para vencer a los temibles enemigos en este RPG de acción. ¡Afronta misiones en solitario o con la ayuda de hasta cuatro...',
            'precio': 38000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/granblue.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sekiro™: Shadows Die Twice - GOTY Edition',
            'descripcion': 'Juego del año - The Game Awards 2019 Mejor juego de acción de 2019 - IGN Traza tu propio camino hacia la venganza en la galardonada aventura de FromSoftware, creadores de Bloodborne y la saga Dark Souls. Véngate. Restituye tu honor. Mata con ingenio.',
            'precio': 47650,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/sekiro.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Palworld',
            'descripcion': 'Este es un juego multijugador de supervivencia en mundo abierto inmenso y original, en el que tendrás que hacerte con unas misteriosas criaturas llamadas Pals, capaces de combatir, construir, cultivar y trabajar en fábricas.',
            'precio': 15500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/palworld.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sea of Thieves',
            'descripcion': 'Sea of Thieves es un exitoso juego de aventuras piratas que ofrece la experiencia pirata por excelencia de saquear tesoros perdidos, batallas intensas, vencer monstruos marinos y más. Sumérgete en esta edición revisada del juego, que incluye acceso a medios digitales de bonificación.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/seaofthieves.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Assassin’s Creed® IV Black Flag',
            'descripcion': 'Año 1715. Los piratas dominaban todo el Caribe y habían establecido su propio gobierno en el que la corrupción, la codicia y la crueldad eran las únicas leyes.Entre estos hombres destacaba un joven y altivo capitán llamado Edward Kenway.',
            'precio': 24900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ac.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'MONSTER HUNTER RISE',
            'descripcion': '¡Acepta el reto y apúntate a la caza! En Monster Hunter Rise, la entrega más reciente de la galardonada y superexitosa serie Monster Hunter, te convertirás en cazador, explorarás mapas nuevos y usarás muchas armas diferentes para acabar con monstruos temibles en una historia totalmente...',
            'precio': 32200,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/monster_hunter.png'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Endless Legend',
            'descripcion': 'Endless Legend es un juego de estrategia y fantasía 4x basado en turnos de los creadores de Endless Space y Dungeon of the Endless. Controla cada aspecto de tu civilización en tu pugna por salvar tu hogar, Auriga. ¡Crea tu propia leyenda!',
            'precio': 11500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/endlesslegend.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Dragons Dogma 2',
            'descripcion': 'Dragon’s Dogma 2 es un juego de rol y acción basado en historia y para un jugador que te permite elegir tu propia experiencia: desde el aspecto de tu Arisen, a tu vocación, tu grupo, cómo afrontar las diferentes situaciones y mucho más, en un mundo de fantasía verdaderamente inmersivo.',
            'precio': 62550,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Dragons_dogma2.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Cities: Skylines II',
            'descripcion': 'Construye una ciudad y haz que prospere con el constructor de ciudades más realista. Pon a prueba tu creatividad y tu resolución de problemas para construir a una escala que nunca experimentaste. Con su simulación y su economía, crea mundos sin límites.',
            'precio': 38100,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Cities_Skylines_II.png'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Age of Mythology: Extended Edition',
            'descripcion': 'Age of Mythology está de vuelta! Elige tu dios y lánzate al campo de batalla en este clásico, mejorado con integración completa de Steamworks y características mejoradas.',
            'precio': 14500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ageofmythology.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'ARK: Survival Ascended',
            'descripcion': '¡Ark se reinventa desde cero en esta próxima generación de tecnología de videojuegos con Unreal Engine 5! Forma una tribu, domestica y cría cientos de dinosaurios únicos y criaturas primitivas, exploran, cree, construyen y luchan hasta la cima de la cadena alimentaria. ¡Tu nuevo mundo te espera!',
            'precio': 41600,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/ark.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Valheim',
            'descripcion': 'Un brutal juego de supervivencia y exploración multijugador, ambientado en un purgatorio generado de forma procedural e inspirado en la cultura vikinga. ¡Lucha, construye y conquista tu viaje en una saga digna de la bendición de Odin!',
            'precio': 7700,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/valheim.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'It Takes Two',
            'descripcion': 'Embárcate en la aventura de tu vida en It Takes Two. Invita a un amigo a acompañarte gratis con el Pase de amigo* para colaborar en una gran variedad de desafíos deliciosamente rompedores.',
            'precio': 31900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/ittakestwo.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Last epoch ',
            'descripcion': 'Descubre el pasado, rehace el futuro. Asciende a una de las 15 clases maestras y explora mazmorras peligrosas, caza botines épicos, forja armas legendarias y maneja el poder de más de cien árboles de habilidades transformadoras. Last Epoch está siendo desarrollado por un equipo de entusiastas apasionados por los juegos de rol de acción.',
            'precio': 18000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/last_epoch.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

