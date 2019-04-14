import filetype
from instagram_private_api_extensions import media as IGMedia
from instagram_private_api import MediaRatios

# snippet from https://github.com/b3nab/instapy-cli
class Media:
    def __init__(self, file):
        self.extension = None
        self.path = file

        self.set_type()

    def prepare(self, story=False):

        ratio = MediaRatios.reel if story else MediaRatios.standard
        size = (1080, 1920) if story else (1080, 1350)

        if self.is_image():
            return IGMedia.prepare_image(self.path, max_size=size, aspect_ratios=ratio)
        elif self.is_video():
            max_time = 15.0 if story else 60.0
            return IGMedia.prepare_video(self.path, max_size=size, aspect_ratios=ratio, max_duration=max_time)

    def is_image(self):
        if self.extension in ['jpg', 'png', 'gif']:
            return True
        return False

    def is_video(self):
        if self.extension in ['jpg', 'png', 'gif']:
            return True
        return False

    def set_type(self):
        self.extension = filetype.guess(self.path).extension
