import unittest
from gui import feedback_button_clicked

class TestGui(unittest.TestCase):
    def test_feedback_button_clicked(self):
        # call the function and assert that it doesn't raise an exception
        self.assertIsNone(feedback_button_clicked())

if __name__ == "__main__":
    unittest.main()