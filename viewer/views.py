from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views.defaults import server_error

from .wrapper import DropboxWrapper

dropbox = DropboxWrapper(settings.DROPBOX_APP_KEY)

# ----------------------------------------------------------------------------
def listfolder(request, url='', uploaded=None, created=None):
    if not dropbox.has_access():
        return HttpResponseRedirect('auth')

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
               'current': levels[-1]['name'],
               'uploaded': uploaded,
               'created': created,
              }
    return render(request, 'viewer/index.html', context)

# ----------------------------------------------------------------------------
def download(request, name):
    fd = dropbox.get_file(name)
    nice_name = name.split('/')[-1]
    response = HttpResponse(fd.read(), content_type="application/octet-stream")
    response['Content-Disposition'] = f'inline; filename={nice_name}'
    return response
    
# ----------------------------------------------------------------------------
def upload(request):
    if request.method == 'POST' and request.FILES['input_file']:
        path = request.POST['folder_path']
        name = dropbox.upload_file(path=path,
                upfile=request.FILES['input_file'])
        return listfolder(None, url=path, uploaded=name)
    return HttpResponseRedirect(reverse('index'))

# ----------------------------------------------------------------------------
def newfolder(request):
    if request.method == 'POST':
        path = request.POST['folder_path']
        name = request.POST['folder_name']
        if len(name) == '':
            return listfolder(None, url=path)
        dropbox.create_folder(path=path, name=name)
        return listfolder(None, url=path, created=name)
    return HttpResponseRedirect(reverse('index'))

# ----------------------------------------------------------------------------
def request_access(request):
    redirect = request.build_absolute_uri(reverse('confirm'))
    print(f"REDIRECT={redirect}")
    url = dropbox.request_access(request.session, redirect)
    context = {'url': url}
    return render(request, 'viewer/access.html', context)

# ----------------------------------------------------------------------------
def confirm_access(request):
    if dropbox.conclude_access(request.GET):
        return HttpResponseRedirect(reverse('index'))
    return server_error(request)
