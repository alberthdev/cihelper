import os
import subprocess
from enum import Enum, unique

FNULL = open(os.devnull, 'w')


@unique
class RunType(Enum):
    NORMAL = dict(stdout=None, stderr=None)
    SILENT = dict(stdout=FNULL, stderr=subprocess.PIPE)
    CAPTURE_STDOUT = dict(stdout=subprocess.PIPE, stderr=None)


def run(cmd, mode=None):
    # Mode Matrix:
    #   mode           | stdout | stderr
    #   ---------------------------------
    #   NORMAL         | None   | None
    #   SILENT         | FNULL  | STDOUT
    #   CAPTURE_STDOUT | PIPE   | None
    #
    # Returns tuple:
    #   (success[bool], None or output str if CAPTURE_STDOUT)

    if mode == None:
        mode = RunType.NORMAL

    if not isinstance(mode, RunType):
        raise RuntimeError("invalid RunType specified: %s" % str(mode))

    cfg_stdout = mode.value["stdout"]
    cfg_stderr = mode.value["stderr"]

    FNULL = None

    p = subprocess.Popen(cmd, stdout=cfg_stdout, stderr=cfg_stderr)
    out, err = p.communicate()

    return (p.returncode == 0, out)
