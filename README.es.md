# gdmty-drf-firebase-auth

Backend de autenticación de Firebase para Django Rest Framework, que permite recibir tokens de Firebase y autenticarlos 
en Django Rest Framework. Opcionalmente, se puede crear un nuevo usuario local en el proceso.

## Requisitos

* Python 3
* Django 4
* Django Rest Framework 3
* Firebase Admin SDK

## Instalación

```bash
$ pip install gdmty-drf-firebase-auth
```

## Configuración

Agregar la aplicación a `INSTALLED_APPS` en `settings.py`.

```python
REST_FRAMEWORK = {
  # ...
  'DEFAULT_AUTHENTICATION_CLASSES': [
    # ...
    'rest_framework.authentication.SessionAuthentication',  # Optional, better to remove for production
    'rest_framework.authentication.BasicAuthentication',  # Optional, better to remove for production
    'gdmty_drf_firebase_auth.authentication.FirebaseAuthentication',
  ]
}
```

la aplicación `gdmty_drf_firebase_auth` viene con las siguientes configuraciones por defecto, las cuales pueden ser 
sobreescritas en el archivo `settings.py` del proyecto. Para mayor comodidad, la mayoría de estas pueden ser configuradas 
desde variables de entorno. Asegúr de anidarlas dentro de `DEFAULT_FIREBASE_AUTH_CONFIG` como se muestra a continuación:

```python
DEFAULT_FIREBASE_AUTH_CONFIG = {
    # allow creation of new local user in db
    'FIREBASE_CREATE_LOCAL_USER': True,
    # attempt to split firebase user.display_name and set local user, first_name and last_name
    'FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME': False,
    # Authorization header prefix, commonly JWT or Bearer (e.g. Bearer <token>)
    'FIREBASE_AUTH_HEADER_PREFIX': 'Bearer',
    # verify that JWT has not been revoked
    'FIREBASE_CHECK_JWT_REVOKED': True,
    # require that firebase user.email_verified is True
    'FIREBASE_AUTH_EMAIL_VERIFICATION': False,
    # function should accept firebase_admin.auth.UserRecord as argument and return str
    'FIREBASE_USERNAME_MAPPING_FUNC': map_firebase_uid_to_username
}
```

Estas configuraciones tienen por defecto los valores expuestos arriba, si no se especifican en el archivo `settings.py` 
del proyecto se toman estos por defecto.

### Configuraciones por proyecto de Firebase

Es necesario utilizar cuentas de servicio de GCP para poder autenticar usuarios de Firebase. La biblioteca original solo 
soporta un solo proyecto; el código original ha sido modificado para permitir más de una cuenta de servicio. Para 
configurar las cuentas de servicio, se debe agregar la siguiente configuración en el archivo `settings.py` del proyecto, 
donde cada elemento corresponde a un proyecto y a su vez, su respectiva cuenta de servicio.

```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

...

FIREBASE_AUTH_SA_KEYFILES = {
    'project-1': os.path.join(BASE_DIR, 'sa', 'project-1-keyfile.json'),
    'project-2': os.path.join(BASE_DIR, 'sa', 'project-2-keyfile.json')
}

FIREBASE_AUTH_PROJECTS = {
    {'PROJECT_ID': 'project-1', 'SERVICE_ACCOUNT_KEY': FIREBASE_AUTH_SA_KEYFILES['project-1']},
    {'PROJECT_ID': 'project-2', 'SERVICE_ACCOUNT_KEY': FIREBASE_AUTH_SA_KEYFILES['project-2']},
}
```

Ahora que se ha configurado la aplicación, se deben ejecutar las migraciones para que los datos de Firebase puedan ser 
almacenados.

```bash
(venv) $ ./manage.py migrate gdmty_drf_firebase_auth
```

Ahora, todo lo necesario para autenticar usuarios de Firebase en Django Rest Framework está listo. Para más información, 
revisar la documentación de [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) y [Firebase Authentication](https://firebase.google.com/docs/auth).

## Contribuir

* Si se utiliza este paquete con una versión de Django o Django Rest Framework diferente a las especificadas en los 
  requisitos, por favor levante un issue y etiquételo como `compatibility`.
* Si se encuentra un error, por favor levante un issue y etiquételo como `bug`.

## Notas adicionales

* Este paquete es una adaptación del paquete [drf-firebase-auth](https://pypi.org/project/drf-firebase-auth/), el cual 
  no está siendo mantenido activamente. El proyecto original solo soporta un proyecto de Firebase por lo que no es 
  posible conectar varios proyectos como origenes de cuentas de Firebase
* El proposito inicial de esta biblioteca fue permitir el inicio de sesión en Django mediante usuario y contraseña de 
  Firebase, sin embargo esta opción fue removida para dejar el paquete más simple y dedicado especificamente a la 
  autenticación mediante IdToken de Firebase.
* Si se desea utilizar la autenticación mediante usuario y contraseña de Firebase, se recomienda utilizar el paquete 
  [gdmty-django-firebase-auth-email-password](https://pypi.org/project/gdmty-django-firebase-auth-email-password/)
* Se recomienda extender el modelo de usuario de Django para agregar los campos que se deseen, y utilizar el campo 
  `email` para almacenar el `uid` de Firebase. Para esto hay que extender la clase AbstractUser y cambiar el atributo 
  USERNAME_FIELD a `email`.

