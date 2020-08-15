#!/usr/bin/env python3
import os
from artifactory import ArtifactoryPath

from .fsutils import get_file_hash


def download_artifact(url, dest=None, validate=True):
    dest = dest or os.path.basename(url)
    path = ArtifactoryPath(url)
    stat = ArtifactoryPath.stat(path)

    with path.open() as fd, open(dest, "wb") as out_fh:
        out_fh.write(fd.read())

    if validate:
        for hash_func in ("md5", "sha1", "sha256"):
            reported_hash = getattr(stat, hash_func)
            actual_hash = get_file_hash(hash_func, dest)

            if reported_hash != actual_hash:
                return None

    return dest
