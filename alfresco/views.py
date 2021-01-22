from com.yoclabo.routing import Router


def browse(request):
    l_router = Router.Router()
    l_router.request = request
    return l_router.run()
