from com.yoclabo.routing import Router


def browse(request):
    l_router = Router.AlfrescoRouter()
    l_router.request = request
    return l_router.run()
