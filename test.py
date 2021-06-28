from pythainlp.tokenize import Tokenizer
from wit import Wit
import psycopg2
import ConAll



DATABASE_URL = 'postgres://dyqpeqyeiurdhq:8badb580880c049e90bb4afe7f36af39b6e7484d387de7653c321569394e498d@ec2-23-23-245-89.compute-1.amazonaws.com:5432/d2gmncd69hhm4g'

mai = ConAll.CreateMainUnit('ทดสอบการเข้าถึง', 2)
mam = mai.regrbo()
mai.update_event('ทดสอบ')
mai.update_backk('2')
mai.update_frontk('5')
mai.update_namlang('e')
mai.update_namna('i')
mai.update_namperm('d d')
mai.close_con()

mal = ConAll.AddUnit('เขา', mam)
mal.update_event('ev')
mal.update_backk('ba')
mal.update_frontk('fr')
mal.update_namlang('nam')
mal.update_namna('edfa')
mal.update_namperm('afs')
mal.update_grob(3)
mal.close_con()

SUB = 'W47IXIHYP2GEG77ZJOWHVHVFGFFWEU2O'
WHO = '56C75TOT6FJGUCN66NJ277Z7BIHJUIEF'
TOQ = 'FLVHKJBETALUJ3GCD7FS5BOKC2EYOOSL'


def extract_value(inp_text, wit_token):
    understanding = Wit(wit_token)
    deep = understanding.message(inp_text)

    try:
        intent_value = deep['data'][0]['__wit__legacy_response']['entities']['intent'][0]['value']
    except KeyError:
        try:
            intent_value = deep['entities']['intent'][0]['value']
        except KeyError:
            intent_value = deep['entities']
    return intent_value

ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')

text = "เธอเป็นยังไงบ้าง"
text_sep = ama.word_tokenize(text)
join_text_sep = ' '.join(text_sep)

sub_available = extract_value(join_text_sep, SUB)
who = extract_value(join_text_sep, WHO)
toq = extract_value(join_text_sep, TOQ)
print(sub_available)
print(who)
print(toq)

text_cut = ama.word_tokenize(text)

ui = []

def salub(text_cut):
    for n, x in enumerate(text_cut):
        ui.append(text_cut[-n-1])
    return ui

print(ui)

#หานามหน้ากริยา
def wicroh(text, dic):
    text_cut = ama.word_tokenize(text)
    for word in text_cut:
        if word in wc:
            if dic[word] == 2:
                mae = []
                print(word)
                k = text_cut[0:text_cut.index(word)]
                m = salub(k)
                whodoo = []
                for ut in m:
                    if ut in wc:
                        if dic[ut] == 1:
                            print(ut)
                            whodoo.append(ut)
                            break
                        else:
                            pass
                    else:
                        pass
                if not whodoo:
                    print("หา 1 ไม่เจอเลยวิเคราะห์โดยใช้ วิท")
                    who = extract_value(text_cut, WHO)
                    whodoo.append(who)
                    break
                else:
                    pass
            else:
                pass
        else:
            print(word + " ไม่พบในคลังคำ")
    print(str(whodoo))

wicroh(text, wtp)
