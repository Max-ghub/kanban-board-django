# python manage.py generate_projects --projects-count 8 --seed 123

import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from management.models.board import Board
from management.models.column import Column
from management.models.project import Project
from management.models.relation_task import RelationTask, RelationTaskType
from management.models.task import Task
from users.models import User


class Command(BaseCommand):
    help = "Generate random projects, boards, columns, tasks and relations linking to random existing users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--projects-count", type=int, default=5, help="Number of projects to create"
        )
        parser.add_argument(
            "--seed", type=int, help="Seed for Faker and random for reproducibility"
        )

    def handle(self, *args, **options):
        fake = Faker()
        seed = options.get("seed")
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
        projects_count = options.get("projects_count", 5)

        user_ids = list(User.objects.values_list("id", flat=True))
        if not user_ids:
            self.stdout.write(
                self.style.ERROR(
                    "Нет пользователей в БД. Сначала создайте пользователей."
                )
            )
            return

        created_projects = 0
        for _ in range(projects_count):
            try:
                with transaction.atomic():
                    owner_id = random.choice(user_ids)
                    owner = User.objects.get(id=owner_id)
                    title = fake.sentence(nb_words=3).rstrip(".")
                    description = fake.text(max_nb_chars=500)
                    is_archived = random.choice([False] * 9 + [True])  # 10% архивных
                    project = Project.objects.create(
                        owner=owner,
                        title=title,
                        description=description,
                        is_archived=is_archived,
                    )
                    other_ids = [uid for uid in user_ids if uid != owner_id]
                    chosen_ids = []
                    if other_ids:
                        max_participants = min(len(other_ids), 5)
                        participant_count = random.randint(0, max_participants)
                        if participant_count > 0:
                            chosen_ids = random.sample(other_ids, k=participant_count)
                            participants = User.objects.filter(id__in=chosen_ids)
                            project.members.add(*participants)
                    project_tasks = []
                    board_count = random.randint(1, 5)
                    for b_index in range(board_count):
                        board_title = fake.word().capitalize()
                        board = Board.objects.create(project=project, title=board_title)
                        col_count = random.randint(1, 7)
                        for c_index in range(col_count):
                            column_title = f"Колонка {c_index+1}"
                            column = Column.objects.create(
                                board=board, title=column_title, order=c_index
                            )
                            task_count = random.randint(2, 5)
                            tasks_created = []
                            for t_index in range(task_count):
                                task_title = fake.sentence(nb_words=4).rstrip(".")
                                task_description = fake.text(max_nb_chars=200)
                                # assignee: случайно из участников + владелец или None
                                possible_ids = [owner_id] + chosen_ids
                                assignee = None
                                if possible_ids and random.random() < 0.5:
                                    assignee_id = random.choice(possible_ids)
                                    assignee = User.objects.get(id=assignee_id)
                                priority = random.choice(
                                    [choice[0] for choice in Task.TaskPriority.choices]
                                )
                                status = random.choice(
                                    [choice[0] for choice in Task.TaskStatus.choices]
                                )
                                estimated_time = round(random.uniform(0.5, 10.0), 2)
                                actual_time = (
                                    round(random.uniform(0.0, estimated_time), 2)
                                    if random.choice([True, False])
                                    else None
                                )
                                task = Task.objects.create(
                                    column=column,
                                    title=task_title,
                                    description=task_description,
                                    parent=None,
                                    assignee=assignee,
                                    priority=priority,
                                    status=status,
                                    estimated_time=estimated_time,
                                    actual_time=actual_time,
                                )
                                tasks_created.append(task)
                                project_tasks.append(task)
                            if tasks_created:
                                for parent_task in tasks_created:
                                    if random.random() < 0.05:
                                        sub_title = fake.sentence(nb_words=3).rstrip(
                                            "."
                                        )
                                        sub_desc = fake.text(max_nb_chars=100)
                                        sub_assignee = None
                                        if possible_ids and random.random() < 0.5:
                                            sub_assignee = User.objects.get(
                                                id=random.choice(possible_ids)
                                            )
                                        sub_priority = random.choice(
                                            [
                                                choice[0]
                                                for choice in Task.TaskPriority.choices
                                            ]
                                        )
                                        sub_status = random.choice(
                                            [
                                                choice[0]
                                                for choice in Task.TaskStatus.choices
                                            ]
                                        )
                                        subtask = Task.objects.create(
                                            column=column,
                                            title=sub_title,
                                            description=sub_desc,
                                            parent=parent_task,
                                            assignee=sub_assignee,
                                            priority=sub_priority,
                                            status=sub_status,
                                            estimated_time=None,
                                            actual_time=None,
                                        )
                                        project_tasks.append(subtask)
                    if len(project_tasks) >= 2:
                        max_rel = max(1, len(project_tasks) // 10)
                        rel_count = random.randint(0, max_rel)
                        types = [choice[0] for choice in RelationTaskType.choices]
                        used_pairs = set()
                        for _ in range(rel_count):
                            from_task, to_task = random.sample(project_tasks, 2)
                            pair = (from_task.id, to_task.id)
                            if pair in used_pairs:
                                continue
                            rel_type = random.choice(types)
                            try:
                                RelationTask.objects.create(
                                    from_task=from_task,
                                    to_task=to_task,
                                    relation_type=rel_type,
                                )
                                used_pairs.add(pair)
                            except Exception:
                                continue
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created project "{project.title}" (owner: {owner}) with {len(project_tasks)} tasks and {rel_count if len(project_tasks)>=2 else 0} relations'
                        )
                    )
                    created_projects += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating project or related data: {e}")
                )
                continue
        self.stdout.write(
            self.style.SUCCESS(f"Total projects created: {created_projects}")
        )
