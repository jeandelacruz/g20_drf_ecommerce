# DRF Boilerplate

## Modelos

- Productos (products)

| columna     | tipo         | constraint   |
| ----------- | ------------ | ------------ |
| id          | SERIAL       | PRIMARY KEY  |
| name        | VARCHAR(80)  | NOT NULL     |
| description | TEXT         | NOT NULL     |
| price       | NUMERIC      | NOT NULL     |
| stock       | INTEGER      | DEFAULT 0    |
| image_url   | VARCHAR(255) | NOT NULL     |
| status      | BOOLEAN      | DEFAULT TRUE |

- Carrito de Compra (shopping_cart)

| columna    | tipo    | constraint           |
| ---------- | ------- | -------------------- |
| id         | SERIAL  | PRIMARY KEY          |
| product_id | INTEGER | FOREIGN KEY NOT NULL |
| user_id    | INTEGER | FOREIGN KEY NOT NULL |
| quantity   | INTEGER | NOT NULL             |

- Pedido de Venta (orders)

| columna        | tipo    | constraint           |
| -------------- | ------- | -------------------- |
| id             | SERIAL  | PRIMARY KEY          |
| user_id        | INTEGER | FOREIGN KEY NOT NULL |
| total_price    | NUMERIC | NOT NULL             |
| subtotal_price | NUMERIC | NOT NULL             |
| igv_price      | NUMERIC | NOT NULL             |
| created_at     | DATE    | DEFAULT DATE_NOW     |

- Detalle de Venta (orders_details)

| columna    | tipo    | constraint           |
| ---------- | ------- | -------------------- |
| id         | SERIAL  | PRIMARY KEY          |
| order_id   | INTEGER | FOREIGN KEY NOT NULL |
| product_id | INTEGER | FOREIGN KEY NOT NULL |
| price      | NUMERIC | NOT NULL             |
| quantity   | INTEGER | NOT NULL             |

## Instalación

```sh
pip install install Django
```

## Iniciar Django

- Crear un proyecto

```sh
django-admin startproject <nombre_proyecto> .
```

- Iniciar proyecto

```sh
python manage.py runserver
```

- Crear superusuario (Se ejecuta despues de las migraciones)

```sh
python manage.py createsuperuser
```

## Apps

1. Modularidad
2. Reutilización
3. Desacoplamiento
4. Escalabilidad
5. Enfoque en la funcionalidad

- Crear una app

```sh
python manage.py startapp <nombre_app>
```

## Migraciones

- Sincronizar o Aplicar migraciones

```sh
python manage.py migrate
```

- Crear una migración

```sh
python manage.py makemigrations
python manage.py makemigrations <nombre_app>
```

## Variables de Entorno

```sh
DEBUG=True

DB_NAME=''
DB_USER='postgres'
DB_PASSWORD=''
DB_HOST='127.0.0.1'
DB_PORT='5432'

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME='@gmail.com'
MAIL_PASSWORD=''
```