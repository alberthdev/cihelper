#!/usr/bin/env python3
import os
import requests
import time

from collections import namedtuple
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class TimeoutRequestsSession(requests.Session):
    def __init__(self, *args, **kwargs):
        self.__default_timeout = None
        if 'timeout' in kwargs:
            self.__default_timeout = kwargs.pop('timeout')
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        if self.__default_timeout:
            kwargs.setdefault('timeout', self.__default_timeout)
        return super(TimeoutRequestsSession, self).request(*args, **kwargs)


SessionSettings = namedtuple("SessionSettings",
                             ["total_retries", "timeout", "backoff_factor", "status_forcelist"])
cached_sessions = {}


def get_session(total_retries=5, timeout=60, backoff_factor=1, status_forcelist=None):
    if not status_forcelist:
        status_forcelist = (500, 502, 503, 504)

    settings = SessionSettings(total_retries=total_retries, timeout=timeout,
                               backoff_factor=backoff_factor, status_forcelist=status_forcelist)

    if settings in cached_sessions:
        return cached_sessions[settings]

    session = TimeoutRequestsSession(timeout=timeout)
    retries = Retry(total=total_retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=status_forcelist)

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("httsp://", HTTPAdapter(max_retries=retries))

    cached_sessions[settings] = session
    return session


def check_url(session, url):
    response = session.get(url)
    return response.status_code < 400


def download_file(session, url, dest=None, chunk_size=8192):
    dl_attempts = 0
    dest = dest or os.path.basename(url)

    with session.get(url, stream=True) as response:
        response.raise_for_status()
        with open(dest, 'wb') as fh:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fh.write(chunk)
    
    return dest

