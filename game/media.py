import pygame
import os

from game import constants


class MediaNotFoundException(Exception):
    pass

class MediaLoadException(Exception):
    pass

class MediaManager(object):
    IMAGE = 'img'
    SOUND = 'snd'
    MUSIC = 'music'
    _images = {}
    _sounds = {}
    _music = {}

    def __getitem__(self, item):
        media_type, dot, key = item.partition('.')
        if media_type == self.IMAGE:
            container = self._images
            lookup = constants.IMAGES
        elif media_type == self.SOUND:
            container = self._sounds
            lookup = constants.SOUNDS
        elif media_type == self.MUSIC:
            container = self._music
            lookup = constants.MUSIC
        else:
            raise MediaLoadException("Invalid media type: '%s'" % media_type)
        if key not in container:
            try:
                path = lookup[key]
            except KeyError:
                raise MediaNotFoundException("Could not find media for key '%s'" % key)
            try:
                container[key] = getattr(self, "load_%s" % media_type)(path)
            except pygame.error, e:
                raise MediaLoadException(str(e))
        return container[key]

    def load_img(self, path):
        return pygame.image.load(os.path.join(constants.IMAGE_PATH, path)).convert()

    def load_snd(self, path):
        return pygame.mixer.Sound(os.path.join(constants.SOUND_PATH, path))

    def load_music(self, path):
        return pygame.mixer.music.load(os.path.join(constants.SOUND_PATH, path))

    def play_music(self, track):
        self.load_music(constants.MUSIC[track])
        pygame.mixer.music.play()

    def fade_music(self, time=500):
        pygame.mixer.music.fadeout(time)

media = MediaManager()
