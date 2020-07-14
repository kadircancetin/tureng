import unittest

from tureng import TurEng


class TestSum(unittest.TestCase):
    tureng = TurEng()

    def test_yes(self):
        trans = self.tureng.translate("yes")

        self.assertFalse(trans.has_error, "Should find the 'yes'")
        self.assertTrue(trans.is_found, "If don't find 'yes', there should be problem")
        self.assertFalse(trans.is_turkish, "Yes is english word.")
        self.assertTrue(trans.is_english, "Yes is english word.")
        self.assertEqual(trans.searched_term, "yes", "Yes is yes. Yes :D")
        self.assertIsNone(trans.suggestions, "Don't suggest for yes")
        self.assertEqual(trans.most_common_translation, "evet", "Most common use of yes is evet")

        self.assertEqual(trans.common_useages[0].tr, "evet", "Yes = evet.")
        self.assertEqual(trans.common_useages[0].eng, "yes", "Yes = evet.")
        self.assertEqual(trans.common_useages[0].type_eng, "n.", "Yes is noun")
        self.assertEqual(trans.common_useages[0].type_tr, "i.", "Evet is isim")

        self.assertIsNotNone(trans.grouped_results, "Should find yes")
        self.assertIsNone(trans.suggestions, "Don't suggest for yes")

    def test_evet(self):
        trans = self.tureng.translate("evet")

        self.assertFalse(trans.has_error, "Should find the 'evet'")
        self.assertTrue(trans.is_found, "If don't find 'evet', there should be problem")
        self.assertTrue(trans.is_turkish, "Evet is turkish word.")
        self.assertFalse(trans.is_english, "Yes is turkish word.")
        self.assertEqual(trans.searched_term, "evet", "Yes is yes. Yes :D")
        self.assertIsNone(trans.suggestions, "Don't suggest for yes")
        self.assertEqual(trans.most_common_translation, "yes", "Most common use of yes is evet")

        self.assertEqual(trans.common_useages[0].tr, "evet", "Yes = evet.")
        self.assertEqual(trans.common_useages[0].eng, "yes", "Yes = evet.")
        self.assertEqual(trans.common_useages[0].type_eng, "n.", "Yes is noun")
        self.assertEqual(trans.common_useages[0].type_tr, "i.", "Evet is isim")

        self.assertIsNotNone(trans.grouped_results, "Shuld find yes")
        self.assertIsNone(trans.suggestions, "Don't suggest for yes")


if __name__ == "__main__":
    unittest.main()
