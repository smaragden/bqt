"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import sys
from contextlib import suppress
import re
import bpy

import subprocess
import shutil

from PySide2.QtGui import QIcon, QImage, QPixmap
from PySide2.QtCore import QByteArray, QObject

from .blender_application import BlenderApplication


class X11BlenderApplication(BlenderApplication):
    """
    X11 implementation of BlenderApplication
    using xprops
    """

    
    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_application_hwnd() -> int:
        """
        This finds the blender application window and collects the
        handler window ID

        Returns int: Handler Window ID
        """

        win_id = -1
        if shutil.which("xdotool") is not None:
            result = subprocess.check_output(["xdotool", "getactivewindow"])
            win_id = int(result)
        elif shutil.which("xprop") is not None:
            regex = r"'\\t(0x[\da-f]+)'.$"
            xprop_cmd = ["xprop", "-root", "32x", "'\t$0'", "_NET_ACTIVE_WINDOW"]
            result = subprocess.check_output(xprop_cmd)
            match = re.search(regex, str(result))
            win_id = int(match.group(1), 16) if match else None
        else:
            print("No tool to get window id", file=sys.stderr)
        return win_id


    def _on_focus_object_changed(self, focus_object: QObject):
        """
        Args:
            QObject focus_object: Object to track focus change
        """

        if focus_object is self.blender_widget:
            if shutil.which("xdotool") is not None:
                result = subprocess.check_call(["xdotool", "windowfocus", self._hwnd])
            else:
                print("No tool to set window focus", file=sys.stderr)

