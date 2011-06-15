import pygame


class SceneError(Exception):
    pass

class SceneManager(object):
    _scenes = {}
    _active_scene = None

    def __init__(self, screen, clock, fps):
        self.screen = screen
        self.clock = clock
        self.fps = fps

    def switch_scene(self, scene_key):
        if scene_key not in self._scenes:
            try:
                scene_class = '%sScene' % scene_key.title()
                module = self._scenes[scene_key] = __import__("game.scenes.%s" % scene_key, {}, {}, scene_class)
                SceneClass = getattr(module, scene_class)
                scene = SceneClass(self)
                self._scenes[scene_key] = scene
                scene.load()
                scene.setup(first_time=True)
            except ImportError, e:
                raise SceneError("Scene %s could not be loaded: %s" % (scene_key, e))
        else:
            try:
                scene = self._scenes[scene_key]
            except KeyError:
                raise SceneError("Scene %s not found" % scene_key)
            scene.setup(first_time=False)
        self._active_scene = scene

    def is_loaded(self, scene_key):
        return scene_key in self._scenes

    def get_state(self, scene_key, key):
        if not self.is_loaded(scene_key):
            return None
        return self._scenes[scene_key].get_state(key)

    def run(self, start_scene):
        self.switch_scene(start_scene)
        while True:
            scene = self._active_scene
            change_scene = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if scene.do_event(event):
                    change_scene = True
                    break

            # Allow events to change the scene - do not render another frame of this one
            if change_scene:
                continue

            scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)


class Scene(object):
    def __init__(self, manager):
        self.manager = manager
        self._state = {}

    def get_state(self, key):
        """Scenes can maintain state variables such as "running" etc. that other scenes can access"""
        return self._state.get(key)

    def set_state(self, key, val):
        self._state[key] = val

    def load(self):
        """The first time a scene is switched to, this method is called"""
        pass

    def setup(self, first_time=False):
        """Any time a scene is switched to, this is called. If we are coming back to a scene that's
        already been shown, first_time will be False"""
        pass

    def render(self, screen):
        """Draw the scene to the screen. Called every clock tick"""
        pass

    def do_event(self, event):
        """Handle a pygame event, such as mouse movement or keyboard input. Returns True if
        we changed scenes, to prevent rendering another frame of the current scene."""
        return False
