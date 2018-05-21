# Instalación

## Instrucciones

Primero clona el repositorio

```bash
# si usas https (muy probablemente sea así)
$ git clone https://github.com/german1608/sip-software.git
# si usas ssh (super recomendado)
$ git clone git@github.com:german1608/sip-software.git
```
Luego, muevete a la carpeta creada

```bash
$ cd sip-software
```

Después, crea un entorno virtual de python. Aquí hay dos opciones.

1. Si usas `virtualenv`:
```bash
# crearlo
virtualenv venv --python=`which python3`
# activarlo
source venv/bin/activate
```
2. Si usas `virtualenvwrapper`:
```bash
# crearlo
mkvirtualenv sip --python=`which python3`
# activarlo
workon sip
```

Instalación de [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).
Instalación de [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

Luego de crear el entorno de desarrollo, proceden a instalar los paquetes necesarios:

```bash
pip install -r requirements.txt
```

Seguidamente, aplicamos las migraciones:

```bash
python manage.py migrate
```

Luego, para verificar que todo funciona correctamente, hagan:

```bash
python manage.py runserver
```

Y abren en el navegador `localhost:8000`. Deberían ver una página con un mensaje que dice Todo funciona fino.

Cualquier inconveniente, notifiquenmelo por favor.
