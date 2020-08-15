import os

from .executils import run


def collect_dynamic_qt_files(windeployqt_tool, dest, exe_file, with_qml=False, qml_dir="qml"):
    os.environ.pop("VCINSTALLDIR", None)

    if with_qml:
        extra_args = ["--qmldir", qml_dir]
    else:
        extra_args = ["--no-angle", "--no-opengl-sw",
                      "--no-system-d3d-compiler"]

    return run([windeployqt_tool] + extra_args + ["--dir", dest, exe_file])
