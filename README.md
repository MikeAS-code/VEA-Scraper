# Vea - Product Scraping Challenge

## Descripción

Desarrollar un crawler en Python capaz de buscar y extraer productos desde el sitio de Vea:

https://www.vea.com.ar/

El crawler deberá trabajar a partir de múltiples combinaciones de **provincia + keyword**, seleccionar una sucursal correspondiente a la provincia solicitada, realizar las búsquedas asociadas y almacenar los productos obtenidos.

El objetivo de la tarea es desarrollar una solución capaz de manejar diferentes contextos de ubicación, múltiples búsquedas por provincia, interacción con el sitio, extracción estructurada de información y persistencia de resultados.

La solución deberá estar preparada para recuperarse ante fallos sin perder las provincias, búsquedas y productos que ya hayan sido procesados.

---

# Input

El crawler deberá aceptar múltiples combinaciones de:

```text
province
keyword
```

Ejemplo conceptual:

```text
chubut "shampoo"
mendoza "crema"
san luis "shampoo"
chubut "perfume"
```

Cada keyword pertenece específicamente a la provincia con la que fue proporcionada.

Por lo tanto:

```text
chubut + shampoo
mendoza + shampoo
```

representan dos búsquedas diferentes.

---

# Reglas del input

Una provincia podrá aparecer múltiples veces siempre que tenga diferentes keywords.

Por ejemplo:

```text
chubut "shampoo"
chubut "perfume"
chubut "crema"
```

es un input válido.

Sin embargo, una misma combinación:

```text
province + keyword
```

no deberá procesarse más de una vez.

Por ejemplo:

```text
chubut "shampoo"
chubut "perfume"
chubut "shampoo"
```

deberá producir únicamente las búsquedas:

```text
chubut + shampoo
chubut + perfume
```

La keyword `shampoo` podrá aparecer nuevamente para otra provincia:

```text
chubut + shampoo
mendoza + shampoo
```

ya que ambas representan contextos de búsqueda diferentes.

---

# Agrupación por provincia

Antes de realizar el scraping, las entradas deberán ser tratadas de forma que las diferentes keywords pertenecientes a una misma provincia puedan procesarse bajo el contexto correspondiente.

Por ejemplo, el input:

```text
chubut "shampoo"
mendoza "crema"
san luis "shampoo"
chubut "perfume"
```

conceptualmente representa:

```text
chubut
    shampoo
    perfume

mendoza
    crema

san luis
    shampoo
```

Esta misma relación deberá reflejarse posteriormente en la estructura del output.

---

# Selección de ubicación

Para cada provincia procesada se deberá establecer correctamente una ubicación dentro del sitio.

El crawler podrá seleccionar **cualquier sucursal disponible perteneciente a la provincia solicitada**.

No existe una sucursal específica o preferida.

Por ejemplo, si debe procesarse:

```text
province: chubut
```

podrá utilizarse cualquier sucursal válida ubicada en Chubut.

La sucursal elegida deberá pertenecer realmente a la provincia solicitada.

---

# Contexto de ubicación

Los productos, precios y promociones disponibles pueden depender de la ubicación seleccionada.

Por esta razón, las búsquedas deberán realizarse bajo el contexto correspondiente a la provincia que se está procesando.

Las keywords asociadas a una provincia deberán procesarse utilizando una sucursal válida de dicha provincia.

No se deberá asumir que los resultados obtenidos bajo una ubicación son válidos para otra.

---

# Datos requeridos

Por cada producto encontrado deberán obtenerse exactamente los siguientes campos:

```python
record['output_name']
record['output_link']
record['output_selling_price']
record['output_image']
record['output_list_price']
record['output_promotion']
```

### `output_name`

Nombre del producto.

### `output_link`

URL correspondiente al producto.

Siempre que sea posible deberá almacenarse como una URL completa y válida.

### `output_selling_price`

Precio actual de venta.

### `output_image`

URL de la imagen principal del producto.

### `output_list_price`

Precio de lista u original.

Cuando no exista un precio de lista diferente, deberá utilizarse un valor vacío o nulo de manera consistente.

### `output_promotion`

Información relacionada con promociones disponibles para el producto.

Cuando no exista una promoción deberá utilizarse un valor vacío o nulo de manera consistente.

---

# Output

El resultado final deberá almacenarse en:

```text
products.json
```

El output deberá agrupar la información utilizando la siguiente jerarquía:

```text
Province
    └── Keyword
            └── Products
```

Cada provincia deberá aparecer **una única vez** en el nivel principal del JSON.

Dentro de `data` deberán encontrarse todas las keywords procesadas para dicha provincia.

Cada keyword deberá contener su correspondiente array de productos.

---

# Estructura requerida

El JSON deberá respetar la siguiente estructura:

```json
[
    {
        "province": "chubut",
        "data": [
            {
                "keyword": "shampoo",
                "products": [
                    {
                        "output_name": "as",
                        "output_link": "as",
                        "output_selling_price": "as",
                        "output_image": "as",
                        "output_list_price": "as",
                        "output_promotion": "as"
                    }
                ]
            },
            {
                "keyword": "perfume",
                "products": [
                    {
                        "output_name": "as",
                        "output_link": "as",
                        "output_selling_price": "as",
                        "output_image": "as",
                        "output_list_price": "as",
                        "output_promotion": "as"
                    }
                ]
            }
        ]
    }
]
```

---

# Ejemplo con múltiples provincias

Para un input como:

```text
chubut "shampoo"
mendoza "crema"
san luis "shampoo"
chubut "perfume"
```

la estructura esperada será:

```json
[
    {
        "province": "chubut",
        "data": [
            {
                "keyword": "shampoo",
                "products": []
            },
            {
                "keyword": "perfume",
                "products": []
            }
        ]
    },
    {
        "province": "mendoza",
        "data": [
            {
                "keyword": "crema",
                "products": []
            }
        ]
    },
    {
        "province": "san luis",
        "data": [
            {
                "keyword": "shampoo",
                "products": []
            }
        ]
    }
]
```

Los arrays `products` deberán contener los productos encontrados para cada búsqueda.

---

# Reglas del output

La estructura final deberá cumplir las siguientes condiciones:

* Una provincia deberá aparecer una única vez.
* Cada provincia deberá contener un campo `data`.
* `data` deberá ser un array.
* Cada keyword deberá aparecer una única vez dentro de su provincia.
* Cada keyword deberá contener un array `products`.
* Los productos deberán pertenecer exclusivamente a la búsqueda correspondiente.
* Una misma keyword podrá existir en diferentes provincias.
* No deberán generarse combinaciones duplicadas.
* El archivo deberá ser JSON válido.

Por ejemplo, esto **no deberá ocurrir**:

```json
[
    {
        "province": "chubut",
        "data": []
    },
    {
        "province": "chubut",
        "data": []
    }
]
```

Las diferentes búsquedas de Chubut deberán encontrarse dentro del mismo objeto.

---

# Búsquedas sin resultados

Una búsqueda puede ejecutarse correctamente y no devolver productos.

En ese caso deberá mantenerse la keyword:

```json
{
    "keyword": "keyword_sin_resultados",
    "products": []
}
```

Esto representa una búsqueda correctamente procesada que no encontró productos.

No deberá confundirse con una búsqueda que falló antes de completarse.

La implementación deberá poder distinguir conceptualmente ambos escenarios para evitar marcar como completado un trabajo que realmente falló.

---

# Persistencia durante la ejecución

El crawler deberá contemplar posibles fallos durante la ejecución.

Los resultados **no deberán guardarse únicamente cuando finalice todo el scraping**.

Los datos obtenidos deberán conservarse progresivamente.

Por ejemplo, si se deben procesar:

```text
chubut
    shampoo
    perfume
    crema
```

y ocurre un fallo mientras se procesa:

```text
crema
```

los resultados correspondientes a:

```text
shampoo
perfume
```

no deberán perderse.

---

# Persistencia entre provincias

La misma regla aplica cuando se procesan diferentes provincias.

Por ejemplo:

```text
chubut
mendoza
san luis
```

Si Chubut y Mendoza fueron procesadas correctamente y ocurre un error durante San Luis, la información obtenida anteriormente deberá continuar disponible.

---

# Recuperación ante fallos

Una nueva ejecución deberá poder considerar la información almacenada previamente.

La solución deberá evitar reprocesar innecesariamente provincias y keywords que ya hayan sido completadas correctamente.

Por ejemplo, si:

```text
chubut + shampoo
chubut + perfume
```

ya fueron procesadas y posteriormente el crawler falló, una nueva ejecución deberá poder identificar ese estado.

La estrategia concreta utilizada para implementar esta recuperación queda a criterio del desarrollador.

Se evaluará especialmente:

* Persistencia progresiva.
* Recuperación ante interrupciones.
* Prevención de pérdida de información.
* Prevención de provincias duplicadas.
* Prevención de keywords duplicadas dentro de una provincia.
* Prevención de productos duplicados.
* Identificación de búsquedas completadas.
* Manejo de búsquedas incompletas.

---

# Manejo de errores

El crawler deberá contemplar situaciones como:

* Provincia inexistente.
* Provincia sin sucursales disponibles.
* Error al seleccionar una sucursal.
* Keyword sin resultados.
* Elementos que no aparecen.
* Cambios inesperados durante la navegación.
* Timeouts.
* Errores de conexión.
* Productos incompletos.
* Campos opcionales inexistentes.
* Errores durante una búsqueda específica.
* Interrupciones inesperadas.

Un error correspondiente a una keyword determinada no debería provocar automáticamente la pérdida de otras búsquedas completadas.

Siempre que sea posible, el crawler deberá continuar procesando el resto de los inputs.

---

# Calidad de los datos

Antes de almacenar cada producto se deberá validar la información obtenida.

Se deberá prestar especial atención a:

* Precios correctamente normalizados.
* URLs completas.
* URLs válidas.
* Imágenes correctamente asociadas.
* Valores opcionales.
* Promociones.
* Caracteres especiales.
* Espacios innecesarios.
* Productos duplicados.

Los datos deberán mantener un formato consistente en todo el archivo.

---

# Logging

La aplicación deberá proporcionar información suficiente para conocer el estado de la ejecución.

Deberá ser posible identificar como mínimo:

* Inicio del crawler.
* Provincia que se está procesando.
* Sucursal seleccionada.
* Keyword actual.
* Cantidad de productos encontrados.
* Productos almacenados.
* Keyword completada.
* Keyword sin resultados.
* Errores.
* Cambio de provincia.
* Finalización del crawler.

La implementación específica del sistema de logs queda a criterio del desarrollador.

---

# Configuración

Los valores configurables deberán mantenerse separados de la lógica principal.

Configuraciones como:

* URL base.
* Timeouts.
* Archivo de salida.
* Configuración necesaria para acceder al sitio.
* Otros valores reutilizables.

deberán centralizarse mediante `config.py` y/o variables de entorno cuando corresponda.

---

# Variables de entorno

El proyecto deberá incluir:

```text
.env
.env.example
```

El archivo `.env` deberá contener las variables locales necesarias para ejecutar el proyecto.

El archivo `.env.example` deberá documentar las variables requeridas sin contener información sensible.

El archivo `.env` no deberá incluirse en el repositorio.

---

# Estructura del proyecto

La estructura mínima requerida será:

```text
project/
│
├── main.py
├── config.py
├── web_driver.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── products.json
```

---

## `main.py`

Será el punto de entrada principal.

Deberá coordinar las responsabilidades necesarias para:

* Recibir los inputs.
* Validar los inputs.
* Agrupar las entradas por provincia.
* Eliminar combinaciones duplicadas.
* Gestionar las provincias.
* Gestionar las keywords.
* Obtener los productos.
* Guardar progresivamente los resultados.
* Recuperar ejecuciones anteriores.
* Manejar errores.

---

## `config.py`

Deberá centralizar la configuración general del proyecto.

Los valores configurables no deberán encontrarse distribuidos innecesariamente por el código.

---

## `web_driver.py`

Deberá concentrar la creación y configuración del mecanismo utilizado para acceder e interactuar con el sitio.

El resto del proyecto deberá reutilizar esta configuración cuando corresponda.

---

## `requirements.txt`

Deberá contener todas las dependencias necesarias.

El proyecto deberá poder instalarse mediante:

```bash
pip install -r requirements.txt
```

---

## `.env`

Contendrá las variables de entorno utilizadas localmente.

No deberá subirse al repositorio.

---

## `.env.example`

Deberá indicar qué variables de entorno necesita el proyecto sin contener valores sensibles reales.

---

## `.gitignore`

Deberá excluir archivos que no deban formar parte del repositorio.

Como mínimo:

```text
.env
__pycache__/
*.pyc
```

---

# Requerimientos técnicos

La solución deberá:

* Estar desarrollada en Python.
* Procesar múltiples combinaciones `province + keyword`.
* Agrupar las entradas por provincia.
* Permitir provincias repetidas con diferentes keywords.
* Permitir una misma keyword en diferentes provincias.
* Evitar combinaciones duplicadas.
* Seleccionar una sucursal válida de cada provincia.
* Mantener correctamente el contexto de ubicación.
* Procesar todas las keywords correspondientes.
* Extraer todos los campos requeridos.
* Agrupar los resultados por provincia.
* Agrupar los productos por keyword dentro de cada provincia.
* Generar un JSON válido.
* Guardar resultados progresivamente.
* Recuperarse ante interrupciones.
* Evitar duplicados.
* Manejar correctamente campos opcionales.
* Manejar búsquedas sin resultados.
* Mantener una estructura de código clara y reutilizable.

La elección de las herramientas y estrategia necesarias para cumplir estos requerimientos queda a criterio del desarrollador.

---

# Entregables

El proyecto deberá contener como mínimo:

```text
main.py
config.py
web_driver.py
requirements.txt
.env.example
.gitignore
products.json
```

El archivo `.env` deberá utilizarse localmente cuando corresponda, pero no deberá incluirse en el repositorio.

---

# Resultado esperado

El resultado final deberá representar la siguiente relación:

```text
Province
│
├── Keyword
│   └── Products
│
├── Keyword
│   └── Products
│
└── Keyword
    └── Products
```

Por ejemplo:

```json
[
    {
        "province": "chubut",
        "data": [
            {
                "keyword": "shampoo",
                "products": [
                    {
                        "output_name": "...",
                        "output_link": "...",
                        "output_selling_price": "...",
                        "output_image": "...",
                        "output_list_price": "...",
                        "output_promotion": "..."
                    }
                ]
            },
            {
                "keyword": "perfume",
                "products": []
            }
        ]
    }
]
```

Cada provincia deberá aparecer una sola vez y contener todas sus búsquedas dentro de `data`.

Cada keyword deberá aparecer una sola vez dentro de su provincia y contener exclusivamente los productos obtenidos para esa búsqueda.

El crawler deberá conservar progresivamente esta estructura durante la ejecución, de manera que los resultados ya obtenidos permanezcan disponibles incluso si una búsqueda posterior falla.

El objetivo de la tarea no es únicamente extraer productos, sino desarrollar una solución capaz de manejar correctamente **ubicaciones, múltiples búsquedas, agrupación de datos, estado, persistencia, recuperación ante fallos y output estructurado**.
