import dataclasses
import unittest
from datetime import date, datetime, timezone
from typing import Any

import tomlenv


class TestRawConfigLoad(unittest.TestCase):
    def test_load_raw_config_simple(self):
        @dataclasses.dataclass
        class Config:
            token: str | None = ""

        raw_config = {"token": "some"}

        obj = Config()
        parser = tomlenv.Parser()
        parser._load_raw_config(obj, raw_config)

        self.assertEqual(obj.token, raw_config["token"])

    def test_load_raw_config_missing_field(self):
        @dataclasses.dataclass
        class Config:
            token: str | None = ""

        raw_config = {"token": "some", "tok": "val"}

        obj = Config()
        parser = tomlenv.Parser()
        parser._load_raw_config(obj, raw_config)

        with self.assertRaises(AttributeError):
            obj.__getattribute__("tok")

    def test_load_raw_config_complex(self):
        @dataclasses.dataclass
        class Config:
            token: str | None = ""
            expiry: datetime | None = None
            enabled: bool = False
            some_list: list[str] = dataclasses.field(default_factory=list)
            some_dict: dict[str, Any] = dataclasses.field(default_factory=dict)

            def __setattr__(self, name, value):
                if name == "expiry":
                    if value:
                        super().__setattr__(
                            name, datetime.fromtimestamp(float(value), timezone.utc)
                        )
                else:
                    super().__setattr__(name, value)

        raw_config = {
            "token": "some",
            "expiry": "1672093282",
            "enabled": True,
            "some_list": ["some"],
            "some_dict": {"key": 0},
        }

        obj = Config()
        parser = tomlenv.Parser()
        parser._load_raw_config(obj, raw_config)

        self.assertEqual(
            obj.expiry, datetime(2022, 12, 26, 22, 21, 22, tzinfo=timezone.utc)
        )
        self.assertEqual(obj.enabled, True)
        self.assertEqual(obj.some_list, ["some"])
        self.assertEqual(obj.some_dict, {"key": 0})


class TestBuildRawConfig(unittest.TestCase):
    def test_build_raw_config_simple(self):
        toml = """
            token = "some"
            expiry = 1979-05-27
            some_list = ["some", "another"]
        """
        parser = tomlenv.Parser()
        raw_config = parser._build_raw_config(toml, environ={})

        self.assertEqual(
            raw_config,
            {
                "expiry": date(1979, 5, 27),
                "some_list": ["some", "another"],
                "token": "some",
            },
        )

    def test_build_raw_config_environ(self):
        toml = """
            token = "some"
            expiry = 1979-05-27
            debug = false
            some_list = ["some", "another"]
        """
        parser = tomlenv.Parser()
        raw_config = parser._build_raw_config(
            toml,
            environ={
                "TOMLENV_EXPIRY": "1994-06-16",
                "TOMLENV_DEBUG": "true",
                "TOMLENV_SOME_LIST": '["new"]',
            },
        )

        self.assertEqual(
            raw_config,
            {
                "expiry": date(1994, 6, 16),
                "debug": True,
                "some_list": ["new"],
                "token": "some",
            },
        )


if __name__ == "__main__":
    unittest.main()
