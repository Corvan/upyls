import unittest

from upyls import MultiIniParser


class TestMultiIniParser(unittest.TestCase):
    def test_simple_ini_config_colon_delimiter(self):
        ini_config = """option1: first option
[section1]
option2: second option
[section2]
option3: third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section1"][0]["option2"][0])
        self.assertEqual("third option", parser["section2"][0]["option3"][0])

    def test_simple_ini_config_equals_delimiter(self):
        ini_config = """option1= first option
[section1]
option2= second option
[section2]
option3= third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section1"][0]["option2"][0])
        self.assertEqual("third option", parser["section2"][0]["option3"][0])

    def test_ini_config_multiple_section_name_colon_delimiter(self):
        ini_config = """option1: first option
[section]
option2: second option
[section]
option3: third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section"][0]["option2"][0])
        self.assertEqual("third option", parser["section"][1]["option3"][0])

    def test_ini_config_multiple_option_name_colon_delimiter(self):
        ini_config = """option1: first option
[section]
option2: second option
option2: second second option
[section]
option3: third option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section"][0]["option2"][0])
        self.assertEqual("second second option", parser["section"][0]["option2"][1])
        self.assertEqual("third option", parser["section"][1]["option3"][0])
        self.assertEqual("second third option", parser["section"][1]["option3"][1])





if __name__ == '__main__':
    unittest.main()
