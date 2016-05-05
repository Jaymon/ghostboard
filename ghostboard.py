from __future__ import print_function
import sys
import os
import argparse
import tempfile
import datetime
import time

import pyperclip


__version__ = "0.1"


def console():
    '''
    cli hook
    return -- integer -- the exit code
    '''
    default_f = os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y-%m-%d-%H:%M.txt"))

    parser = argparse.ArgumentParser(description='Listen to the system clipboard and write out new contents to file')
    parser.add_argument('filepath', nargs="?", default=default_f, help='File where clipboard contents will be written')
    #parser.add_argument('--clean', action='store_true', help='If Passed in, paste with no metadata')

    parser.add_argument("--version", "-V", action='version', version="%(prog)s {}".format(__version__))

    args = parser.parse_args()


    last_paste_txt = pyperclip.paste()
    backoff = 0.25
    cb_count = 0
    with open(args.filepath, "a") as fp:

        fileno = fp.fileno()

        while True:
            time.sleep(backoff)

            paste_txt = pyperclip.paste()
            if paste_txt != last_paste_txt:
                cb_count += 1
                print("{}. {}".format(cb_count, paste_txt))

                fp.write(paste_txt)
                fp.write("\n")
                fp.flush()
                os.fsync(fileno)

                last_paste_txt = paste_txt
                backoff = 0.25

            else:
                backoff = 0.25
                #backoff = min(backoff + 1, 60)

    return 0


if __name__ == "__main__":
    sys.exit(console())

