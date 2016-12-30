# coding: UTF-8

#名詞のリストを返す
def get_noun(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if not noun[0] == "EOS":
            try:
                if noun[3] == "名詞" or noun[11] == "\"品詞推定:名詞\"":
                    items.append(noun[0])
            except IndexError:
                print "IndexError"
    return items

#名詞と動詞と形容詞のリストを返す
def get_noun_verb_adjective(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if not noun[0] == "EOS":
            try:
                if noun[3] == "名詞" or noun[11] == "\"品詞推定:名詞\"" or noun[3] == "動詞" or noun[3] == "形容詞":
                    items.append(noun[0])
            except IndexError:
                print "IndexError"
    return items

if __name__ == '__main__':
    pass

