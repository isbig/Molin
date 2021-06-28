from pythainlp.tokenize import Tokenizer
import time
import random
import DBcon
import config
import Anpasa

text = 'ฉันกำลังเดินไปอยู่'
dfa = Anpasa.AnText(text)
ea = dfa.tran_type()
dr = dfa.madas()
print(text)
print(str(ea))
print(dr)

sad = config.DATABASE_URL
print('man')
mun = DBcon.FinePum(sad)
print('fads')
tf = 'me'
mann = DBcon.DataConnect(sad)
mann.sai_word_type('หนัก', 2)
mann.close_con()
pan3 = mun.last_ks(tf)
pan4 = mun.find_ks_name(tf)
pan5 = mun.find_ks_name(tf)
pan6 = mun.find_pum(pan5)
print(str(pan3))
print(str(pan4)+"_____")
print(str(pan5)+"_____")
print(str(pan6))
DBcon.FinePum(sad).close_con()

current_milli_time = lambda: int(round(time.time() * 1000))

print(current_milli_time())
k = random.randint(0,9)
mama = str(current_milli_time())+str(k)
print(mama)
print(mama)

text1 = "วันนี้ไปห้าง ไปร้านหนังสือด้วยนะครับช่วยต่อลมหายใจร้านหนังสือ"
ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
sms = ama.word_tokenize(text1)
print(sms)

de = [1, 2, 3]
de2 = [3, 4, 5]
for x in de:
    print(x)