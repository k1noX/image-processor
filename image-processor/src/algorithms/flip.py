from algorithms import ImageAlgorithm
from PIL import Image, ImageOps

class FlipAlgoithm(ImageAlgorithm):
    @classmethod
    def process(cls, image: Image.Image, params: dict) -> Image.Image:
        if not "orientation" in params:
            raise ImageAlgorithm.ParamsError("Required parameters: orientation")
        if params["orientation"] == "vertical":
            return ImageOps.mirror(image)
        elif params["orientation"] == "horizontal":
            return ImageOps.flip(image)
        else:
            raise ImageAlgorithm.ParamsError("Orientation should be either horizontal or vertical")