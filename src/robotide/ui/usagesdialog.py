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

from robotide.widgets import (Dialog, VirtualList, VerticalSizer, ImageList,
                              ImageProvider)


class UsagesDialog(Dialog):

    def __init__(self, name, usages):
        self._name = name
        self._selection_listeners = []
        self.usages = UsagesListModel(usages)
        title = "'%s' - %d usages" % (name, self.usages.total_usages)
        Dialog.__init__(self, title=title, size=(650, 400))
        self.SetSizer(VerticalSizer())
        usage_list = VirtualList(self, ['Location', 'Usage', 'Source'],
                                 self.usages)
        usage_list.add_selection_listener(self._usage_selected)
        self.Sizer.add_expanding(usage_list)

    def _usage_selected(self, idx):
        for listener in self._selection_listeners:
            listener(self.usages.usage(idx).item.parent, self._name)

    def add_selection_listener(self, listener):
        self._selection_listeners.append(listener)


class UsagesListModel(object):

    def __init__(self, usages):
        self._usages = usages
        self.images = self._create_image_list()

    def _create_image_list(self):
        images = ImageList(16, 16)
        provider = ImageProvider()
        images.add(provider.TESTCASEIMG)
        images.add(provider.KEYWORDIMG)
        images.add(provider.DATAFILEIMG)
        images.add(provider.DATADIRIMG)
        return images

    def item_text(self, row, col):
        u = self._usages[row]
        return [u.location,  u.usage, u.source][col]

    def image(self, item):
        # TODO: better mechanism for item type recognition
        parent_type = self._usages[item].parent
        return {'TestCaseController': 0,
                'UserKeywordController': 1,
                'TestCaseFileController': 2,
                'ResourceFileController': 2,
                'TestDataDirectoryController': 3}.get(parent_type, -1)

    def usage(self, idx):
        return self._usages[idx]

    @property
    def total_usages(self):
        return sum(u.count for u in self._usages)

    @property
    def count(self):
        return len(self._usages)
