import pygame
class Bindings():
    def __init__(self, parent):
        self.parent = parent
        self.key_mapping = {
           # "v":["i"]
        }

        self.temp_binding = None
        self.temp_binding_map = []
        self.accepting_binding = False

    def save_key_binding(self):
        self.key_mapping[self.temp_binding] = self.temp_binding_map
        self.temp_binding = None
        self.temp_binding_map = []
        self.accepting_binding = False

    def has_binding(self, key):
        return key in self.key_mapping

    def use_keybinding(self, key):
        for keys in self.key_mapping[key]:
            self.parent.set_next_key(keys)