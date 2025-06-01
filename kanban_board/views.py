from django.http import HttpResponse


def index_page(request):

    return HttpResponse(
        '<h1><a href="admin/">Admin</a></h1>'
        + '<h1><a href="users/">Users</a></h1>'
        + '<h1><a href="registration/">Register</a></h1>'
        + '<h1><a href="auth/">Auth</a></h1>'
        + '<h1><a href="api/">API</a></h1>'
    )
