# Filename: test_authorization.py

"""
Test the lendingclub2.authorization module
"""

# Standard libraries
import os
from configparser import ConfigParser

# lendingclub2
from lendingclub2.config import API_KEY_ENV, CONFIG_FPATH, CONFIG_FPATH_ENV
from lendingclub2.authorization import Authorization


class TestAuthAPIEnv(object):
    @classmethod
    def setup_class(cls):
        cls.clean = False
        if not os.getenv(API_KEY_ENV):
            os.environ[API_KEY_ENV] = 'foo'
            cls.clean = True

    @classmethod
    def teardown_class(cls):
        # Required workaround
        if Authorization._CODE is not None:
            Authorization._CODE = None

        if cls.clean:
            del os.environ[API_KEY_ENV]

    def test_api_key_env(self):
        auth = Authorization()
        assert auth.key == os.getenv(API_KEY_ENV)


class TestAuthAPIConfigEnv(object):
    @classmethod
    def setup_class(cls):
        cls.key = 'bar'

        cls.restore = None
        if os.getenv(API_KEY_ENV):
            cls.restore = os.getenv(API_KEY_ENV)
            del os.environ[API_KEY_ENV]

        cls.old_config_fpath = None

        create_new_config = True
        if os.getenv(CONFIG_FPATH_ENV) is not None:
            cls.old_config_fpath = os.getenv(CONFIG_FPATH_ENV)

            config = ConfigParser()
            with open(os.getenv(CONFIG_FPATH_ENV)) as fin:
                config.read_file(fin)

            try:
                _ = config['access']['api_key']
                create_new_config = False
            except KeyError:
                pass

        if create_new_config:
            fpath = 'test_config.cfg'
            os.environ[CONFIG_FPATH_ENV] = fpath

            config = ConfigParser()
            config['access'] = {
                'api_key': cls.key,
            }

            with open(fpath, mode='w') as fout:
                config.write(fout)

    @classmethod
    def teardown_class(cls):
        # Required workaround
        if Authorization._CODE is not None:
            Authorization._CODE = None

        if cls.restore is not None:
            os.environ[API_KEY_ENV] = cls.restore

        if os.path.exists(os.environ[CONFIG_FPATH_ENV]):
            os.remove(os.environ[CONFIG_FPATH_ENV])

        if cls.old_config_fpath is None:
            del os.environ[CONFIG_FPATH_ENV]
        else:
            os.environ[CONFIG_FPATH_ENV] = cls.old_config_fpath

    def test_api_config_env(self):
        auth = Authorization()
        assert auth.key == TestAuthAPIConfigEnv.key
