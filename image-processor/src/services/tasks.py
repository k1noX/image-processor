import typing
from injectors.db import DbContainer
from models.task import Task, TaskStatus
from injectors.pika import PikaContainer


class FileException(Exception):
    pass


class FileNotFoundException(FileException):
    pass


class FileNotImageException(FileException):
    pass


class TaskRestartException(Exception):
    pass


def get_all_tasks() -> typing.List[dict]:
    with DbContainer.get_db_session(engine=DbContainer.engine) as session:
        tasks: list[Task] = session.query(Task).all()
        return [task.dict for task in tasks]


def create_task(file_ids: list[int], algorithm: str, params: dict):
    with DbContainer.get_db_session(engine=DbContainer.engine) as session:
        if isinstance(file_ids, list):
            task_ids = []
            for id in file_ids:
                task = Task(source_id=id, algorithm=algorithm, params=params)
                session.add(task)
                session.commit()

                task_ids.append(task.id)

                connection = PikaContainer.connection
                channel = PikaContainer.get_channel(connection)

            for id in task_ids:
                channel.basic_publish(
                    exchange=PikaContainer.config.rabbitmq_exchange,
                    routing_key=PikaContainer.config.rabbitmq_routing_key,
                    body=f"{id}",
                )

            connection.close()

            return task_ids

    return []


def get_task_by_id(id: int) -> Task:
    with DbContainer.get_db_session(engine=DbContainer.engine) as session:
        task: Task = session.query(Task).filter(Task.id == id).first()
        return task


def restart_task(id: int) -> Task:
    with DbContainer.get_db_session(engine=DbContainer.engine) as session:
        task: Task = session.query(Task).filter(Task.id == id).first()
        if task.status == TaskStatus.FINISHED or task.status == TaskStatus.PROCESSING:
            raise TaskRestartException(
                "Task has already been finished or is in process!"
            )
        task.status = TaskStatus.PENDING

        connection = PikaContainer.connection
        channel = PikaContainer.get_channel(connection)

        channel.basic_publish(
            exchange=PikaContainer.config.rabbitmq_exchange,
            routing_key=PikaContainer.config.rabbitmq_routing_key,
            body=f"{id}",
        )

        connection.close()

        return task
