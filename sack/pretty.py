"""
    Make output prietter.
    ProgressBar inspired by HiBench
"""
try:
    # Python >= 3.2
    import shutil
    columns, rows = shutil.get_terminal_size((80, 20))
except:
    # Python < 3.2
    import os
    rows, columns = os.popen('stty size', 'r').read().split()

import sys

Color = {
    'Black': '\033[0;30m',
    'Red': '\033[1;31m',
    'White': '\033[1;37m',
    'Purple': '\033[0;35m',
    'Cyan': '\033[0;36m',
    'On_Red': '\033[41m',
    'On_Yellow': '\033[43m',
    'On_Blue': '\033[44m',
    'On_White': '\033[47m',
    'Color_Off': '\033[0m'
}


class ProgressBar(object):
    def __init__(self):
        pass

# ### setters
    @property
    def set_tab(self):
        return self._set_tab

    @classmethod
    @set_tab.setter
    def set_tab(self, value):
        self._set_tab = value

    @property
    def text(self):
        return self._text

    @classmethod
    @text.setter
    def text(self, value):
        self._text = value


# ### staticmethods
    @staticmethod
    def step(text, progress, line_width):
        pos = int(progress)
        if len(text) < line_width:
            text += " " * (line_width - len(text))
        text = "{Black}{On_Yellow}{s1}{On_Blue}{s2}{Color_Off}\r".format(
            s1=text[:pos],
            s2=text[pos:], **Color)
        sys.stdout.write(text)

    @staticmethod
    def hook(count, chunk, total):
        downloaded = int(count * chunk)
        if downloaded > total:
            downloaded = total
        ProgressBar.step("{} {}/{}".format(
            ProgressBar.text, downloaded, total),
            int(count / (total / chunk / columns)), columns)
