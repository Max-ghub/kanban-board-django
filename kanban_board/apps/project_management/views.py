from django.http import HttpResponse


def index_page(request):
    return HttpResponse('<h1><a href="admin/">Admin</a></h1>')
