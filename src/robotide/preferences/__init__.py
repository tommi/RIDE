#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os


from.settings import Settings, initialize_settings
from .editor import PreferenceEditor
from .widgets import (PreferencesPanel, PreferencesComboBox,
    PreferencesColorPicker)
from .imports import ImportPreferences
from .saving import SavingPreferences
from .colors import ColorPreferences


class RideSettings(Settings):

    def __init__(self):
        default_path = os.path.join(os.path.dirname(__file__), 'settings.cfg')
        user_path = initialize_settings('ride', default_path)
        Settings.__init__(self, user_path)
        self._settings_dir = os.path.dirname(user_path)
        self.set('install root', os.path.dirname(os.path.dirname(__file__)))

    def get_path(self, *parts):
        """Returns path which combines settings directory and given parts."""
        return os.path.join(self._settings_dir, *parts)


class Preferences(object):

    def __init__(self, settings):
        self.settings = settings
        self._preference_panels = []
        self._add_builtin_preferences()

    @property
    def preference_panels(self):
        return self._preference_panels

    def add(self, prefrence_ui):
        if prefrence_ui not in self._preference_panels:
            self._preference_panels.append(prefrence_ui)

    def remove(self):
        if panel_class in self._preference_panels:
            self._preference_panels.remove(panel_class)

    def _add_builtin_preferences(self):
        self.add(SavingPreferences)
        self.add(ImportPreferences)
        self.add(ColorPreferences)
