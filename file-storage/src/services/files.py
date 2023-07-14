from utils.file_utils import is_allowed_name
from models.file import File
import re, datetime, os
from injectors.db import DbContainer
from injectors.app import AppContainer

app_config = AppContainer.config


class NameNotAllowed(Exception):
    pass


def create_file(f, name, extension, comment=None):
    if not is_allowed_name(name):
        return NameNotAllowed("File Name Not Allowed!"), 400

    with DbContainer.get_db_session(DbContainer.engine) as session:
        name = re.sub(f"{extension}$", "", name)
        created_at = datetime.datetime.now()

        file = File(
            name=name,
            extension=extension,
            created_at=created_at,
        )

        if comment is not None:
            file.comment = comment

        session.add(file)
        session.commit()

    with DbContainer.get_db_session(DbContainer.engine) as session:
        file = (
            session.query(File)
            .filter(File.name == name)
            .filter(File.extension == extension)
            .filter(File.created_at == created_at)
            .first()
        )

        f.save(os.path.join(app_config.path, str(file.id) + file.extension))

        file.size = os.stat(
            os.path.join(app_config.path, str(file.id) + file.extension)
        ).st_size

        response = file.dict

        session.commit()

        return response
