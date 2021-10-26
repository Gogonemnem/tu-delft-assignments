import os
import unittest

from project.settings.settings_tab import Settings

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
path = os.path.join(fileDirectory, 'settings_file_test')


class TestSettings(unittest.TestCase):

    def test_read_settings(self):
        # Read the current settings in the list
        settings_list = Settings.read_settings(path)
        self.assertEqual(settings_list, ['40', '8'])

    def test_save_settings(self):
        # First read the current settings, by reusing test_read_settings
        # And use the save_settings to make sure the settings are at the original values
        # This is to make sure the test works, even if another tests failed
        # or if someone edited the settings_test_file
        Settings.save_settings(path, [40, 8])
        self.test_read_settings()

        # Give the settings a new list to save
        # The length of the list doesn't matter
        Settings.save_settings(path, [56, 9, 14])

        # Test if the settings are changed by using read_settings
        settings_list = Settings.read_settings(path)
        self.assertEqual(settings_list, ['56', '9', '14'])

        # Reset the file by saving the original settings and check if it succeeded
        Settings.save_settings(path, [40, 8])
        self.test_read_settings()
