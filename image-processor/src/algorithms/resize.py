from algorithms import ImageAlgorithm
from PIL import Image


class ResizeAlgorithm(ImageAlgorithm):
    @classmethod
    def process(cls, image: Image.Image, params: dict) -> Image.Image:
        if not all(k in params for k in ("width", "height")):
            raise ImageAlgorithm.ParamsError("Required parameters: width, height")
        width = params["width"]
        height = params["height"]

        image = image.resize((width, height), Image.Resampling.LANCZOS)
        return image
