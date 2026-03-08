import sys

from tipster.cmd import cli
from tipster.cmd.tips import tips_new

if len(sys.argv) == 1 or (
    len(sys.argv) == 3 and sys.argv[1] == "tips" and sys.argv[2] == "new"
):
    tips_new(None)
else:
    if __name__ == "__main__":
        cli()
