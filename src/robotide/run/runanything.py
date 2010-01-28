#  Copyright 2008-2009 Nokia Siemens Networks Oyj
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

import wx

from robotide.pluginapi import Plugin, ActionInfo, SeparatorInfo
from robotide.run.configmanagerui import ConfigManagerDialog
from robotide.run.ui import Runner


class RunAnything(Plugin):

    def __init__(self, app):
        Plugin.__init__(self, app, default_settings={'configs': []})

    def enable(self):
        self._create_menu(_RunConfigs(self.configs))

    def OnManageConfigurations(self, event):
        dlg = ConfigManagerDialog(_RunConfigs(self.configs))
        if dlg.ShowModal() == wx.ID_OK:
            configs = _RunConfigs(dlg.get_data())
            self.save_setting('configs', configs.data_to_save())
            self._create_menu(configs)
        dlg.Destroy()

    def _create_menu(self, configs):
        self.unregister_actions()
        self.register_action(ActionInfo('Run', 'Manage Run Configurations',
                                        self.OnManageConfigurations))
        self.register_action(SeparatorInfo('Run'))
        for index, cfg in enumerate(configs):
            self._add_config_to_menu(cfg, index+1)

    def _add_config_to_menu(self, config, index):
        def run(event):
            Runner(config, self.notebook).run()
        info = ActionInfo('Run', name='%d: %s' % (index, config.name),
                          doc=config.help, action=run)
        self.register_action(info)


class _RunConfigs(object):

    def __init__(self, saved_data):
        self._configs = []
        for item in saved_data:
            self.add(item[0], item[1], item[2])

    def __iter__(self):
        return iter(self._configs)

    def __len__(self):
        return len(self._configs)

    def add(self, name, command, doc):
        config = _RunConfig(name, command, doc)
        self._configs.append(config)
        return config

    def swap(self, index1, index2):
        self._configs[index1], self._configs[index2] = \
                self._configs[index2], self._configs[index1]

    def pop(self, index):
        self._configs.pop(index)

    def data_to_save(self):
        return [ (c.name, c.command, c.doc) for c in self._configs ]


class _RunConfig(object):
    help = property(lambda self: '%s (%s)' % (self.doc, self.command))

    def __init__(self, name, command, doc):
        self.name = name
        self.command = command
        self.doc = doc
        self._finished = False
        self._error = False
