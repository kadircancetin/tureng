import unittest

from tureng import TurEng


class TestSum(unittest.TestCase):
    tureng = TurEng()

    def test_yes(self):
        trans = self.tureng.translate("yes")

        self.assertFalse(trans.has_error, "Should find the 'yes'")
        self.assertTrue(trans.is_found, "If don't find 'yes', there should be problem")
        self.assertEqual(trans.searched_term, "yes", "Yes is yes :D")
        self.assertIsNone(trans.suggestions, "Don't suggest for yes")

        self.assertEqual(trans.best_tr_translation.tr, "evet")
        self.assertEqual(trans.best_tr_translation.en, "yes")

        self.assertTrue("evet" in trans.all_tr_translation_str)

        self.assertLess(0, len(trans.en2tr_groups))
        self.assertEqual(len(trans.tr2en_groups), 0)

    def test_evet(self):
        trans = self.tureng.translate("evet")

        self.assertFalse(trans.has_error)
        self.assertTrue(trans.is_found)
        self.assertEqual(trans.searched_term, "evet")
        self.assertIsNone(trans.suggestions)

        self.assertEqual(trans.best_en_translation.tr, "evet")
        self.assertEqual(trans.best_en_translation.en, "yes")

        self.assertTrue("yes" in trans.all_en_translation_str)

        self.assertLess(0, len(trans.tr2en_groups))
        self.assertEqual(len(trans.en2tr_groups), 0)

    def test_suggest(self):
        trans = self.tureng.translate("yys")
        self.assertFalse(trans.is_found)
        self.assertTrue("yes" in trans.suggestions)

    def test_smoke_test(self):
        words = ["evet", "quadrile", "yes", "yys", "şflkjsadşflkjşsaldkfjaşsldkfjşsaldjfşlaskdjf"]

        for word in words:
            tmp = self.tureng.translate(word)
            tmp.best_tr_translation
            tmp.best_en_translation
            tmp.tr2en_groups
            tmp.en2tr_groups
            tmp.best_en2tr_group
            tmp.best_tr2en_group
            tmp.all_en_translation_str
            tmp.all_tr_translation_str

        tmp = self.tureng.translate("evet")
        first_word = tmp.best_tr_translation

        for i in tmp.grouped_results:
            i.add_word(first_word)

        second_group = tmp.grouped_results[1]
        self.assertEqual(second_group.words[0].tr, "evet")


if __name__ == "__main__":
    unittest.main()
