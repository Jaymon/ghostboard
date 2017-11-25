# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import sys
import os
import argparse
import tempfile
import datetime
import time
import codecs

import pyperclip


__version__ = "0.1.1"


def console():
    '''
    cli hook
    return -- integer -- the exit code
    '''
    default_f = os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y-%m-%d-%H:%M.txt"))

    parser = argparse.ArgumentParser(description='Listen to the system clipboard and write out new contents to file')
    parser.add_argument('filepath', nargs="?", default=default_f, help='File where clipboard contents will be written')
    #parser.add_argument('--clean', action='store_true', help='If Passed in, paste with no metadata')
    parser.add_argument(
        '--delim', '-d', '--postfix', '-p',
        dest="delim",
        default="\n",
        type=lambda x: x.decode('string_escape'),
        help='will be added to the end of the pasted text'
    )
    parser.add_argument("--version", "-V", action='version', version="%(prog)s {}".format(__version__))

    args = parser.parse_args()
    delim = args.delim
    last_paste_txt = pyperclip.paste()
    backoff = 0.15
    cb_count = 0
    with codecs.open(args.filepath, encoding='utf-8', mode='a') as fp:

        print("Hello! Pasted text will be written to {}\n".format(args.filepath))
        fileno = fp.fileno()

        try:
            while True:
                time.sleep(backoff)

                paste_txt = pyperclip.paste()
                if paste_txt != last_paste_txt:
                    if paste_txt and not paste_txt.isspace():
                        cb_count += 1
                        print("{}. {}".format(cb_count, paste_txt))

                        fp.write(paste_txt)
                        fp.write(delim)
                        fp.flush()
                        os.fsync(fileno)

                        last_paste_txt = paste_txt

        except KeyboardInterrupt:
            print("\nGoodbye! Pasted text was written to {}".format(args.filepath))

    return 0


if __name__ == "__main__":
    sys.exit(console())

