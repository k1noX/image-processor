import re
from werkzeug.utils import secure_filename

from injectors.app import AppContainer


symbols = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA",
)

pairs = {ord(a): ord(b) for a, b in zip(*symbols)}


def is_allowed_name(name) -> str:
    return not any((c in name) for c in AppContainer.config.forbidden_characters)


def is_allowed_folder_name(name: str) -> str:
    return not any((c in name) for c in AppContainer.config.forbidden_characters)


def transliterate(name: str) -> str:
    return name.translate(pairs)


def secure_path(path: str) -> str:
    secure_location = ""
    path = transliterate(path)
    location_parts = re.split("\/", path)

    for folder in location_parts:
        secure_location += secure_filename(folder) + "/"

    secure_location = secure_location.rstrip("/")

    return secure_location


def secure_file_path(path: str) -> tuple:
    secure_location = ""
    path = transliterate(path)
    location_parts = re.split("\/", path)

    for folder in location_parts[:-1]:
        secure_location += secure_filename(folder) + "/"

    filename = secure_filename(location_parts[-1])

    secure_location = secure_location.rstrip("/")

    return secure_location, filename
