# coding:utf-8

import unittest
import json
import os

class ImageTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        with open('weapon.json', 'r') as f:
            json_data = json.load(f)
        for buki in json_data:
            path = "images/main/" + buki["name"]["ja_JP"] + ".png"
            self.assertTrue(os.path.isfile(path), f"{path} does not exist")

    def test_weapon(self):
        with open('weapon.json', 'r') as f:
            json_data = json.load(f)
        for buki in json_data:
            path = "images/weapon/" + buki["name"]["ja_JP"] + ".jpg"
            self.assertTrue(os.path.isfile(path), f"{path} does not exist")

if __name__ == "__main__":
    unittest.main()
