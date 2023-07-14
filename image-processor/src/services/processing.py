from models.task import Task, TaskStatus
from injectors.db import DbContainer
from injectors.app import ApiContainer
import requests
from handler.handler import Handler
from io import BytesIO
from PIL import Image
from sqlalchemy.orm.exc import NoResultFound
import logging


def process_task(id: int):
    with DbContainer.get_db_session(DbContainer.engine) as session:
        try:
            task: Task = session.query(Task).filter(Task.id == id).first()
            task.status = TaskStatus.PROCESSING
            session.commit()
        except NoResultFound:
            return

    with DbContainer.get_db_session(DbContainer.engine) as session:
        try:
            task: Task = session.query(Task).filter(Task.id == id).first()
        except NoResultFound:
            return
        file_url = ApiContainer.get_file_download_url(task.source_id)
        print(file_url)
        try:
            r = requests.get(file_url, allow_redirects=True)
            print(r.status_code)
            print(r.headers["Content-Type"])
            r.raise_for_status()
            if r.headers["Content-Type"].startswith("image"):
                image_request = requests.get(file_url, allow_redirects=True)
                image_io = BytesIO(image_request.content)
                image = Image.open(image_io)
                logging.info(
                    "Received %d bytes from request to %s",
                    image_io.tell(),
                    image_request.url,
                )
                result = Handler.handle(image, task.algorithm, task.params)
                with BytesIO() as output:
                    result.save(output, format="PNG")
                    logging.info(
                        "Received %d bytes as %s output", output.tell(), task.algorithm
                    )
                    output.seek(0)
                    logging.info(
                        "Trying to send %d bytes to %s",
                        output.tell(),
                        ApiContainer.config.base_image_url,
                    )
                    post_req = requests.post(
                        ApiContainer.config.base_image_url,
                        files={
                            "file": (
                                f"task_{task.id}_result.png",
                                output,
                                "multipart/form-data",
                            )
                        },
                    )
                    logging.info("Request finished with code %d", post_req.status_code)
                    post_req.raise_for_status()
                    new_file = post_req.json()
                    task.result_id = new_file["id"]
                    task.status = TaskStatus.FINISHED
            else:
                task.status = TaskStatus.ERROR
        except Exception as e:
            logging.error(Exception.with_traceback())
            task.status = TaskStatus.ERROR
        session.commit()


def finish_task_with_error(id: int, error: str = ""):
    with DbContainer.get_db_session(DbContainer.engine) as session:
        try:
            task: Task = session.query(Task).filter(Task.id == id).first()
            task.status = TaskStatus.ERROR
            session.commit()
        except NoResultFound:
            return
