from PIL import Image


class ImageAlgorithm:
    class ParamsError(Exception):
        pass

    class AlgorithmError(Exception):
        pass

    @classmethod
    def process(cls, image: Image.Image, params: dict) -> Image.Image:
        pass
