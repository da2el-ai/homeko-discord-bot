"""
参考サイト
https://corkborg.github.io/wd14-tagger-standalone/
"""

from typing import Generator, Iterable
from pathlib import Path
from PIL import Image
from .tagger.interrogator import Interrogator
from .tagger.interrogators import interrogators

DEFAULT_MODEL = 'wd14-convnextv2.v1'

interrogator = interrogators[DEFAULT_MODEL]
interrogator.use_cpu()

class Tagger:
    threshold = 0.35

    """
    画像からタグを抽出
    """
    @classmethod
    def get_tags(cls, image_path: Path, tag_escape=False, exclude_tags = set()) -> dict[str, float]:
        im = Image.open(image_path)
        result = interrogator.interrogate(im)

        return Interrogator.postprocess_tags(
            result[1],
            threshold=cls.threshold,
            escape_tag=tag_escape,
            replace_underscore=tag_escape,
            exclude_tags=exclude_tags)
    
    

