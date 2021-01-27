# dropboxviewer

This is a Django sample app to visualize and download files from a 
Dropbox account.

## Dependencies

In order to run this app, you must install `django` and `dropbox` from the
PyPI repository.

```
pip install django
pip install dropbox
```

The following versions were used when the app was written:

* Python 3.9.1
* Django 3.1.5
* Dropbox Python API 11.0.0

## Running

From a terminal, run the following command inside the project folder:

```
python manage.py runserver
```

To access the app, open the following link in your browser:

```
http://localhost:8000/viewer/
```

It will possibly display an error message, saying it cannot access a Dropbox
account. To link this app to an account, use the following instructions.

## Connecting to a Dropbox account

Two steps are necessary to connect the app to a Dropbox account. First,
you must register this app with Dropbox to obtain a valid key. (Usually, this
means using your Dropbox account to register a new app.) It's important that
you require full access to the client's account, otherwise the app will just
display an empty folder. 

Second, you must require access to a Dropbox account, which will be 
visualized by the app. You may use your own account as well as any.

This process is partially automated by executing the following script:

```
python dropbox_access.py
```

It will follow the above steps, asking you to access some Dropbox web pages
in order to obtain authorization tokens. Follow the instructions and input the
tokens accordingly. At the end, the script will check if the connection was
successful. If not, remove the newly-created file ``dropbox.key`` and try
again.

## What does it do?

If all the configuration was done correctly, the app should display the
contents of the linked Dropbox account. You can browse its folders and download
its files.

## Credits

This sample is based on examples and ideas taken from API
documentations and other sources. In particular, it incorporates a 
custom ``Storage`` class written by Anthony Monthe, also available 
from the PyPI package ``django-storages``.

