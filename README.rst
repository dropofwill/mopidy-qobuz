****************
Mopidy-Qobuz
****************

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Qobuz <https://www.qobuz.com/>`_.

Requires a Qobuz subscription.


Installation
============

This is a fork of `mopidy-qobuz` that uses `qobuz-dl` to fetch app_id/app_secret from the qobuz web app instead of using a harcoded (and now blocked) kodi api key.

Currently not published anywhere, so muse be installed as a dev extension. Clone source code and run:

```
pip3 install --upgrade --editable .
```


Configuration
=============

Before starting Mopidy, you must add your Qobuz username and password
to the Mopidy configuration file::

    [qobuz]
    username = alice
    password = secret

Or put qobuz password in your OS keyring:

```bash
keyring mopidy-qobuz password
...<enter password in prompt>...
```


Project resources
=================

- `Source code <https://github.com/dropofwill/mopidy-qobuz>`_


Disclaimer
==========

This application uses the Qobuz API but is not certified by Qobuz. Any use of the API implies your full acceptance of the Qobuz General Terms and Conditions (http://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf)
