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
        # Required workaround
        if Authorization._CODE is not None:
            Authorization._CODE = None

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

        cls.clean = create_new_config
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

        if cls.clean:
            os.remove(os.environ[CONFIG_FPATH_ENV])

        if cls.old_config_fpath is None:
            del os.environ[CONFIG_FPATH_ENV]
        else:
            os.environ[CONFIG_FPATH_ENV] = cls.old_config_fpath

    def test_api_config_env(self):
        auth = Authorization()
        assert auth.key == TestAuthAPIConfigEnv.key


class TestAuthAPIConfig(object):
    @classmethod
    def setup_class(cls):
        cls.key = 'bar'

        cls.restore = None
        if os.getenv(API_KEY_ENV):
            cls.restore = os.getenv(API_KEY_ENV)
            del os.environ[API_KEY_ENV]

        cls.old_config_fpath = None
        if os.getenv(CONFIG_FPATH_ENV) is not None:
            cls.old_config_fpath = os.getenv(CONFIG_FPATH_ENV)
            del os.environ[CONFIG_FPATH_ENV]

        cls.config = None
        if os.path.exists(CONFIG_FPATH):
            cls.config = ConfigParser()
            with open(CONFIG_FPATH) as fin:
                cls.config.read_file(fin)

            try:
                _ = cls.config['access']['api_key']
            except KeyError:
                pass

        config = ConfigParser()
        config['access'] = {
            'api_key': cls.key,
        }

        with open(CONFIG_FPATH, mode='w') as fout:
            config.write(fout)

    @classmethod
    def teardown_class(cls):
        # Required workaround
        if Authorization._CODE is not None:
            Authorization._CODE = None

        if cls.restore is not None:
            os.environ[API_KEY_ENV] = cls.restore

        if cls.old_config_fpath is not None:
            os.environ[CONFIG_FPATH_ENV] = cls.old_config_fpath

        if cls.config is not None:
            with open(CONFIG_FPATH, mode='w') as fout:
                cls.config.write(fout)
        else:
            os.remove(CONFIG_FPATH)

    def test_api_config_env(self):
        auth = Authorization()
        assert auth.key == TestAuthAPIConfig.key

    def test_header(self):
        auth = Authorization()
        assert auth.header == {'Authorization': auth.key}
