from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import hasher, Paste

def decode_and_get_paste(hashid):
    decoded_id = hasher.decode(hashid)
    if len(decoded_id) == 0:
        raise Http404()

    paste = get_object_or_404(Paste, pk=decoded_id[0])
    return paste

def view_paste(request, hashid, template='paste/paste.html'):
    paste = decode_and_get_paste(hashid)
    context = {'paste': paste}
    return render(request, template, context)

def view_paste_raw(request, hashid):
    paste = decode_and_get_paste(hashid)
    return HttpResponse(paste.data, content_type='text/plain')
