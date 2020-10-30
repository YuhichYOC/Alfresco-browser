from .rooting import rooter


def browse(request):
    if request.GET.get('id') is not None:
        return rooter.another(request, request.GET.get('id'), request.GET.get('skip_count'))
    else:
        return rooter.root(request)
