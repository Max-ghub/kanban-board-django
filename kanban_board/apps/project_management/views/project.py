from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.utils.request import parse_request_json_data, validate_request_json_data
from users.models import User

from ..models.project import Project


def get_project(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404(f'Проект "{project_id}" не существует')


@method_decorator(csrf_exempt, name="dispatch")
class ProjectView(View):
    def get(self, request, project_id):
        """Получение проекта по id"""
        project = get_project(project_id)

        return JsonResponse(
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "owner": project.owner.id,
                "members": list(project.members.values_list("id", flat=True)),
                "is_archived": project.is_archived,
            }
        )

    def post(self, request):
        """Создание проекта"""
        try:
            project_data = parse_request_json_data(request)

            required = ["title", "owner_id", "members_id"]
            validate_request_json_data(project_data, required)

            title = project_data.get("title")
            description = project_data.get("description", "")
            owner = User.objects.get(id=project_data.get("owner_id"))
            members = User.objects.filter(id__in=project_data.get("members_id"))
            is_archived = project_data.get("is_archived", False)

            project = Project.objects.create(
                title=title,
                description=description,
                owner=owner,
                is_archived=is_archived,
            )
            project.members.set(members)

            return JsonResponse(
                {
                    "message": f'Проект "{title}" успешно создан',
                    "data": {
                        "title": project.title,
                        "description": project.description,
                        "owner": project.owner.id,
                        "members": list(project.members.values_list("id", flat=True)),
                        "is_archived": project.is_archived,
                    },
                },
                status=201,
            )

        except ValidationError as e:
            return JsonResponse({"error": e.message})

    def delete(self, request, project_id):
        """Удаление проекта"""
        project = get_project(project_id)
        project.delete()
        return JsonResponse({"message": f'Проект "{project.title}" успешно удалён'})

    def put(self, request, project_id):
        """Обновление проекта"""
        project = get_project(project_id)
        project_data = parse_request_json_data(request)

        project.title = project_data.get("title", project.title)
        project.description = project_data.get("description", project.description)
        project.owner = User.objects.get(id=project_data.get("owner", project.owner))
        project.members.set(
            User.objects.filter(id__in=project_data.get("members", project.members))
        )
        project.is_archived = project_data.get("is_archived", project.is_archived)

        project.save()

        return JsonResponse(
            {
                "message": f'Проект "{project.id}" успешно обнавлён',
                "data": {
                    "title": project.title,
                    "description": project.description,
                    "owner": project.owner.id,
                    "members": list(project.members.values_list("id", flat=True)),
                    "is_archived": project.is_archived,
                },
            },
            status=201,
        )
