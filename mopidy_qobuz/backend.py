from __future__ import unicode_literals

import binascii
import keyring
import logging
import os
import threading
import pykka
import qobuz
from itertools import cycle
from qobuz_dl import spoofbuz
from mopidy import backend, httpclient
from mopidy_qobuz import library, playback, browse


logger = logging.getLogger(__name__)

KEYRING_NAME = "mopidy-qobuz"

def get_keyring(key: str):
    logger.info(f"key {key} keyring {KEYRING_NAME}")
    return keyring.get_password(KEYRING_NAME, key)

def set_keying(key: str, val: str):
    keyring.set_password(KEYRING_NAME, key, val)

class MopidyQobuzConfigError(Exception):
    pass

class QobuzBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(QobuzBackend, self).__init__()

        self._config = config
        self._session = None

        self.library = library.QobuzLibraryProvider(backend=self)
        self.playback = playback.QobuzPlaybackProvider(
            audio=audio, backend=self
        )
        # self.playlists = playlists.QobuzPlaylistsProvider(backend=self)
        self.uri_schemes = ["qobuz"]

    def get_qobuz_password(self):
        conf_pw = self._config["qobuz"]["password"]
        if (conf_pw):
            logger.info("found in conf")
            return conf_pw
        else:
            maybe_pw = get_keyring("password")
            if (maybe_pw):
                logger.info("found in keyring")
                return maybe_pw
            else:
                raise MopidyQobuzConfigError(
                        "No qobuz password in keyring or conf file")

    def get_qobuz_app_id_and_secret(self, username, password):
        maybe_app = get_keyring("app_id")
        maybe_secret = get_keyring("app_secret")

        if (maybe_app and
            maybe_secret and
            self.secret_works(username, password, maybe_app, maybe_secret)):
            return [maybe_app, maybe_secret]
        else:
            spoofer = spoofbuz.Spoofer()
            maybe_app = spoofer.getAppId()
            logger.info(spoofer.getSecrets())
            maybe_secrets = [
                secret for secret in spoofer.getSecrets().values() if secret]

            for secret in maybe_secrets:
                res = self.secret_works(username, password, maybe_app, secret)
                if res:
                    set_keying("app_id", maybe_app)
                    set_keying("app_secret", secret)
                    return [maybe_app, secret]
            raise MopidyQobuzConfigError("No secrets worked")

    def secret_works(self, username, password, app_id, app_secret) -> bool:
        self.register(username, password, app_id, app_secret)
        try:
            res = qobuz.api.request(
                "userLibrary/getAlbumsList",
                signed = True,
                user_auth_token=self._session.auth_token)
            return True
        except Exception as e:
            logger.info(e)
            return False

    def register(self, username, password, app_id, app_secret):
        qobuz.api.register_app(
            app_id=app_id, app_secret=app_secret)
        self._session = qobuz.User(username, password)

    def on_start(self):
        self._actor_proxy = self.actor_ref.proxy()

        username = self._config["qobuz"]["username"]
        password = self.get_qobuz_password()
        [app_id, app_secret] = self.get_qobuz_app_id_and_secret(
                username, password)
        self.register(
            username, password, app_id, app_secret)
