import unittest
import tkinter as tk
from main import main

class TestMainApplication(unittest.TestCase):

    def test_main_application(self):
        root = tk.Tk()
        with self.assertRaises(SystemExit) as cm:
            main(root)
        self.assertEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
