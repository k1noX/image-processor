from algorithms import ImageAlgorithm
from PIL import Image, ImageOps


class RotateAlgorithm(ImageAlgorithm):
    @classmethod
    def process(cls, image: Image.Image, params: dict) -> Image.Image:
        if not "direction" in params:
            raise ImageAlgorithm.ParamsError("Required parameters: direction")
        if params["direction"] == "clockwise":
            return image.rotate(90, expand=True)
        if params["direction"] == "counterclockwise":
            return image.rotate(-90, expand=True)
        else:
            raise ImageAlgorithm.ParamsError(
                "Direction should be either clockwise or counterclockwise"
            )
