# coding: UTF-8

#名詞のリストを返す
def get_noun(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if not noun[0] == "EOS":
            if noun[3] == "名詞":
                items.append(noun[0])
    return items

if __name__ == '__main__':
    pass

