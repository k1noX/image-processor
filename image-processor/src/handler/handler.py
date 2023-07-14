from algorithms import rotate, flip, resize, ImageAlgorithm
from PIL import Image
import typing
import logging


class Handler:
    class HandlerError(Exception):
        pass

    allowed_algorithms: typing.Dict["str", ImageAlgorithm] = {
        "resize": resize.ResizeAlgorithm,
        "rotate": rotate.RotateAlgorithm,
        "flip": flip.FlipAlgoithm,
    }

    @classmethod
    def handle(cls, image: Image.Image, algorithm: str, params: dict) -> Image.Image:
        if algorithm in Handler.allowed_algorithms:
            logging.info(
                "Starting processing with %s with params %s", algorithm, str(params)
            )
            return Handler.allowed_algorithms[algorithm].process(image, params)
        else:
            logging.info(f"{algorithm} is not allowed algorithm name!")
            raise Handler.HandlerError(f"{algorithm} is not allowed algorithm name!")
