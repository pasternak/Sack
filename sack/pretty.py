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
    'On_Red': '\033[41m',
    'On_Yellow': '\033[43m',
    'On_Blue': '\033[44m',
    'Color_Off': '\033[0m'
}


class ProgressBar(object):

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
        ProgressBar.step(" Progress: {}/{}".format(
            downloaded, total),
            int(count / (total / chunk / columns)), columns)
