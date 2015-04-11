from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import hasher, Paste

def view_paste(request, hashid, template='paste/paste.html'):
    decoded_id = hasher.decode(hashid)
    if len(decoded_id) == 0:
        raise Http404()

    paste = get_object_or_404(Paste, pk=decoded_id[0])
    context = {'paste': paste}
    return render(request, template, context)
