import json

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
        self.is_english = resp_dic["MobileResult"]["IsTRToEN"]
        self.is_turkish = not self.is_english
        self.searched_term = resp_dic["MobileResult"]["Term"]

        self.grouped_results = None
        self.common_useages = None
        self.most_common_translation = None
        self.suggestions = None

        if self.is_found:
            self.grouped_results = self.__get_group_results(resp_dic)
            self.common_useages = [
                self.grouped_results[typ]
                for typ, lst in self.grouped_results.items()
                if "Common Usage" in typ
            ][0]
            self.most_common_translation = self.common_useages[0].translated
        else:
            self.suggestions = resp_dic["MobileResult"]["Suggestions"]

    def __get_group_results(self, resp_dic):
        results = resp_dic["MobileResult"]["Results"]
        categories = dict()

        for result in results:
            if result["CategoryEN"] in categories:
                categories[result["CategoryEN"]].append(
                    TurEngWord(result, self.searched_term)
                )
            else:
                categories[result["CategoryEN"]] = [
                    TurEngWord(result, self.searched_term)
                ]
        return categories


class TurEngWord:
    def __init__(self, word_dic, searched_term):
        self.group_eng = word_dic["CategoryEN"]
        self.group_tr = word_dic["CategoryTR"]
        self.type_eng = word_dic["TypeEN"]
        self.type_tr = word_dic["TypeTR"]
        self.eng = searched_term
        self.tr = word_dic["Term"]
        self.translated = self.tr

        if "(tr->en)" in word_dic["CategoryEN"]:
            self.tr, self.eng = self.eng, self.tr
            self.translated = self.eng

    def __repr__(self):
        return f"({self.tr} -> {self.eng})"
