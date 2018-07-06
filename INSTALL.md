
# Para la instalación se lista la siguiente serie de pasos:

Paso 1: Primero clona el repositorio

```bash
# Si ud. usa https (muy probablemente sea así), la línea de comando que debes usar es la siguiente:
$ git clone https://github.com/german1608/sip-software.git
# Si uud. usa ssh (se sugieresu uso), la líena de comando que debes usa es la siguiente:
$ git clone git@github.com:german1608/sip-software.git
```
Posteriormente, se debe ubicar en la carpeta creada llamada 'sip-software', usando la siguiente 
línea de comando:

```bash
$ cd sip-software
```

Paso 2: 
Después, debe proceder a crear un entorno virtual de python. Se listan dos opciones para lograr esto:

Opción 1:
Si usa `virtualenv`:
```bash
# Primero lo crea:
virtualenv venv --python=`which python3`
# Después lo activa:
source venv/bin/activate
```
Opción 2:

Si usa `virtualenvwrapper`:
```bash
# Primero lo crea:
mkvirtualenv sip --python=`which python3`
# Después lo activa:
workon sip
```
Para mayor información acerca de la creación del entorno virtual puede visitar los siguientes enlaces:
Instalación de [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).
Instalación de [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

Paso 3: Luego de crear el entorno de desarrollo, proceden a instalar los paquetes necesarios:

```bash
pip install -r requirements.txt
```

Seguidamente, aplicamos las migraciones:

```bash
python manage.py migrate
```

Luego, para verificar que todo funciona correctamente, se procede a ejecutar:

```bash
python manage.py runserver
```

Finalmente en el navegador se coloca `localhost:8000`. Ya en este punto debe aparecer el sistema SIP ejecutandose 
exitosamente.
