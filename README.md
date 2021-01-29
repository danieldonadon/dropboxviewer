# dropboxviewer

This is a Django sample app that allows basic file manipulation using Dropbox
storage. After connecting to a Dropbox account, you can navigate its folders,
download its files, and upload new documents. This app was created as a 
programming exercise to learn Django.


## Installing and running

It's suggested that you run this app in a 
[Python virtual environment](https://docs.python.org/3/tutorial/venv.html).
To install the app, execute the following commands in a terminal:

```
    git clone https://www.github.com/danieldonadon/dropboxviewer.git
    cd dropboxviewer
    pip install -r requirements.txt
    python manage.py migrate
```

Then, to run the app, execute:

```
    python manage.py runserver
```

To access the app, open the following link in your browser: http://localhost:8000/viewer/


## Connecting to a Dropbox account

The first time you run the app, it will request authorization to access a 
Dropbox account. Simple click on the "Request" button and follow the 
instruction. This app requests full access to all files in order to 
function as intended. You may rest assured, however, that the app will never
delete any document at all, but be aware that uploading files _may_ modify
existing documents of the same name.

You may opt to create your own app registration at 
[Dropbox Developer's App Console](https://www.dropbox.com/developers/apps).
If you do, replace the ``DROPBOX_APP_KEY`` on ``dropboxviewer/settings.py``
with your own app key.


## Credits

This sample is based on examples and ideas taken from API
documentations and many other sources. In particular, it incorporates a 
custom ``Storage`` class written by Anthony Monthe, also available 
from the PyPI package ``django-storages``.

