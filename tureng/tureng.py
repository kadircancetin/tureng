import json
import re

import requests


class TurEng:
    url = "http://ws.tureng.com/TurengSearchServiceV4.svc/Search"

    def translate(self, word):
        data = {"Term": word}
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        obj = json.loads(response.text)
        return TranslatedResult(obj)


class TranslatedResult:
    def __init__(self, resp_dic):
        self.has_error = not resp_dic["IsSuccessful"]
        self.is_found = resp_dic["MobileResult"]["IsFound"]
        self.searched_term = resp_dic["MobileResult"]["Term"]

        self.grouped_results = None
        self.suggestions = None

        if self.is_found:
            self.grouped_results = self.__get_group_results(resp_dic)
        else:
            self.suggestions = resp_dic["MobileResult"]["Suggestions"]

    def group_search(self, patern, attribution="name_en"):
        return [x for x in self.grouped_results if re.match(patern, getattr(x, attribution))]

    @property
    def all_tr_translation_str(self):
        words = []
        for group in self.en2tr_groups:
            words.extend([x.tr for x in group.words])
        return words

    @property
    def all_en_translation_str(self):
        words = []
        for group in self.tr2en_groups:
            words.extend([x.en for x in group.words])
        return words

    @property
    def best_tr_translation(self):
        if self.best_en2tr_group:
            return self.best_en2tr_group.words[0]
        return None

    @property
    def best_en_translation(self):
        if self.best_tr2en_group:
            return self.best_tr2en_group.words[0]
        return None

    @property
    def tr2en_groups(self):
        if not self.is_found:
            return []
        return [x for x in self.grouped_results if x.orj_lang == "tr"]

    @property
    def en2tr_groups(self):
        if not self.is_found:
            return []
        return [x for x in self.grouped_results if x.orj_lang == "en"]

    @property
    def best_en2tr_group(self):
        if not self.is_found:
            return None

        for i in self.grouped_results:
            if i.orj_lang == "en":
                return i
        return None

    @property
    def best_tr2en_group(self):
        if not self.is_found:
            return None

        for i in self.grouped_results:
            if i.orj_lang == "tr":
                return i
        return None

    def __get_group_results(self, resp_dic):
        results = resp_dic["MobileResult"]["Results"]
        categories_str = dict()

        for result in results:
            c_name = "{}--{}--{}".format(
                result["CategoryEN"][:-9],
                result["CategoryTR"][:-9],
                result["CategoryTR"][-7:-5]
            )

            if c_name in categories_str:
                categories_str[c_name].append(
                    TurEngWord(result, self.searched_term)
                )
            else:
                categories_str[c_name] = [
                    TurEngWord(result, self.searched_term)
                ]

        categories = []
        for category, words in categories_str.items():
            name_en, name_tr, orj_lang = category.split("--")
            group = TurEngGroup(orj_lang=orj_lang, name_en=name_en, name_tr=name_tr)

            categories.append(group)
            for word in words:
                group.add_word(word)

        return categories


class TurEngGroup:
    def __init__(self, orj_lang, name_en, name_tr):
        self.name_tr = name_tr
        self.name_en = name_en
        self.orj_lang = orj_lang
        self.trans_lang = "en"
        if self.orj_lang == "en":
            self.trans_lang = "tr"
        self.words = []

    def add_word(self, word):
        self.words.append(word)

    def __repr__(self):
        return "({}->{}) {}-{} Group [{} word]".format(
            self.orj_lang, self.trans_lang, self.name_tr, self.name_en, len(self.words)
        )


class TurEngWord:
    def __init__(self, word_dic, searched_term):
        self.group_en = word_dic["CategoryEN"]
        self.group_tr = word_dic["CategoryTR"]
        self.type_en = word_dic["TypeEN"]
        self.type_tr = word_dic["TypeTR"]
        self.en = searched_term
        self.tr = word_dic["Term"]
        self.orj_lang = self.en

        if "(tr->en)" in word_dic["CategoryEN"]:
            self.tr, self.en = self.en, self.tr
            self.orj_lang = self.tr

    def __repr__(self):
        if self.orj_lang == self.tr:
            return self.tr + " -> " + self.en
        return self.en + " -> " + self.tr


if __name__ == "__main__":
    tureng = TurEng()
    s = tureng.translate("evet")
    print(s.best_en_translation)
