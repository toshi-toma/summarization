# coding: UTF-8
import sys
def get_domain(domain):
    data = domain[1:-1]
    sp = data.split(" ")
    for dom in sp:
        sp_domain = dom.split(":")
        if sp_domain[0] == "ドメイン":
            return sp_domain[1]


def get_title_domain(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if noun[0] == "@": continue
        if len(noun) > 12:
            for st in noun[12:]:
                noun[11] += " " + st
        if not noun[0] == "EOS":
            try:
                if noun[11] == "NIL":
                    pass
                elif "ドメイン" in noun[11]:
                    items.append(get_domain(noun[11]))
            except IndexError:
                print "IndexError"
    return items


def get_features(text, domain):
    items = [0,0,0,0]
    line = text.splitlines()
    for n,i in enumerate(line):
        noun = i.split(" ")
        if noun[0] == "@": continue
        if len(noun) > 12:
            for st in noun[12:]:
                noun[11] += " " + st
        if not noun[0] == "EOS":
            try:
                # 先頭語が助詞(0 or 1)
                if n == 0:
                    if noun[3] == "接続詞" or noun[3] == "助詞":
                        items[0] = 1
                # 数詞があるか(0 or 1)
                if noun[5] == "数詞":
                    items[1] = 1
                # 人名があるか(0 or 1)
                if noun[5] == "人名":
                    items[2] = 1
                # ドメインの一致(0 or 1)
                if noun[11] == "NIL":
                    pass
                elif "ドメイン" in noun[11]:
                    dom = get_domain(noun[11])
                    if dom in domain:
                        items[3] = 1
            except IndexError:
                print "IndexError"
    return items

#単語のリストを返す
def get_words(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if noun[0] == "@": continue
        if not noun[0] == "EOS":
            try:
                items.append(noun[0])
            except IndexError:
                print "IndexError"
                return 0
    return items
#名詞のリストを返す
def get_noun(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if noun[0] == "@": continue
        if len(noun) > 12:
            for st in noun[12:]:
                noun[11] += " " + st
        if not noun[0] == "EOS":
            try:
                if noun[3] == "名詞" or noun[11] == "\"品詞推定:名詞\"":
                    items.append(noun[0])
            except IndexError:
                print "IndexError"
                return 0
    return items

#名詞と動詞と形容詞のリストを返す
def get_noun_verb_adjective(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if noun[0] == "@": continue
        if len(noun) > 12:
            for st in noun[12:]:
                noun[11] += " " + st
        if not noun[0] == "EOS":
            try:
                if noun[3] == "名詞" or noun[11] == "\"品詞推定:名詞\"" or noun[3] == "動詞" or noun[3] == "形容詞":
                    items.append(noun[0])
            except IndexError:
                print "IndexError"
                return 0
    return items

if __name__ == '__main__':
    pass

