# snippet from https://github.com/b3nab/instapy-cli

import os
import json
import codecs
from instagram_private_api import Client, ClientCompatPatch, ClientCookieExpiredError, ClientLoginRequiredError

from .media import Media

import warnings
warnings.filterwarnings("ignore")

class ClientApi(object):
    def __init__(self, username, password):
        self.settings = 'settings.json'
        self.login(username, password)

    def login(self, username, password):

        try:
            if os.path.isfile(self.settings):
                self.client_api = Client(username, password,
                on_login=lambda x: self.write_cache(x, self.settings))
            else:
                cached_settings = self.cache()
                self.device_id = cached_settings.get('device_id')
                self.client_api = Client(username,
                                         password,
                                         settings=cached_settings)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            self.client_api = Client(username,
                                     password,
                                     device_id=self.device_id,
                                     on_login=lambda x: self.write_cache(x, self.settings))

    def upload(self, file, caption='', story=False):

        upload_completed = None
        media = Media(file)
        res = None

        image_data, image_size = media.prepare(story)

        try:
            if media.is_image():
                image_data, image_size = media.prepare(story)

                if story:
                    res = self.client_api.post_photo_story(image_data, image_size)
                else:
                    res = self.client_api.post_photo(image_data, image_size, caption=caption)

            elif media.is_video():
                video_data, video_size, video_duration, video_thumbnail = media.prepare(story)
                if story:
                    res = self.client_api.post_video_story(video_data, video_size, video_duration, video_thumbnail)
                else:
                    res = self.client_api.post_video(video_data, video_size, video_duration, video_thumbnail, caption=caption)
            else:
                raise Exception('Media is not a recognized file type, use only images and videos.')


        except Exception as e:
            print("Exception: ", e)
            upload_completed = False
            return False

        finally:
            upload_completed = True
            #print('Result: ', res)
            return True

    def write_cache(self, api, settings):
        with open(self.settings, 'w') as cached_settings:
            json.dump(api.settings, cached_settings, default=self.to_json)
            #print('SAVED: {0!s}'.format(settings))

    @property
    def cache(self):
        with open(self.settings, 'r') as cached_settings:
            return json.load(cached_settings, object_hook=self.from_json)

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object
