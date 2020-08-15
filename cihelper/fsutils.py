import errno
import glob
import hashlib
import os
import shutils


def get_file_hash(hashlib_func_name, filename, blocksize=2**20):
    if not hasattr(hashlib, hashlib_func_name):
        raise RuntimeError("invalid hashlib_func_name=%s" % hashlib_func_name)

    m = getattr(hashlib, hashlib_func_name)()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)

    return m.hexdigest()

# tzot @ StackOverflow:
# http://stackoverflow.com/a/600612
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

def get_file_list(directory):
    file_list = []
    root_parts = len(directory.split(os.sep))
    
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            # Delete root folder from path to form archive path!
            arc_path = os.sep.join(full_path.split(os.sep)[root_parts:])
            file_list.append([full_path, arc_path])
    
    return file_list

def glob_copy(glob_from, dest):
    for fn in glob.glob(glob_from):
        shutils.copyfile(fn, os.path.join(dest, os.path.basename(fn)))
