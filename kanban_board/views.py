from django.http import HttpResponse


def index_page(request):

    return HttpResponse(
        '<h1><a href="admin/">Admin</a></h1>'
        + '<h1><a href="api/users/">Users</a></h1>'
        + '<h1><a href="api/registration/">Register</a></h1>'
        + '<h1><a href="api/auth/">Auth</a></h1>'
        + '<h1><a href="api/">API</a></h1>'
        + '<h1><a href="swagger/">Swagger UI</a></h1>'
        + '<h1><a href="redoc/">Swagger ReDoc</a></h1>'
    )
