from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .wrapper import DropboxWrapper

dropbox = DropboxWrapper(settings.DROPBOX_KEY_FILE)

def listfolder(request, url=''):
    if not dropbox.has_access():
        return HttpResponse("Cannot access Dropbox! " + \
            f"Check connectivity with dropbox_access.py.")

    files = dropbox.listdir('' if len(url) == 0 else ('/' + url))

    levels = [{'url': '', 'name': ''}]
    if url != '':
        for part in url.split('/'):
            up = levels[-1]['url']
            info = {'url' : ((up + '/') if len(up) > 0 else '') + part,
                    'name': part}
            levels.append(info)

    context = {'url': url, 
               'levels': levels,
               'files': files,
               'current': levels[-1]['name']}
    return render(request, 'viewer/index.html', context)


def download(request, name):
    if not dropbox.has_access():
        return HttpResponse("Cannot access Dropbox! " + \
            f"Check connectivity with dropbox_access.py.")

    fd = dropbox.get_file(name)
    nice_name = name.split('/')[-1]
    response = HttpResponse(fd.read(), content_type="application/octet-stream")
    response['Content-Disposition'] = f'inline; filename={nice_name}'
    return response
    
