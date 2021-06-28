from pythainlp.tokenize import Tokenizer
import DBcon
import config
import os


class AnText:
    def __init__(self, text):
        try:
            db_url = os.getenv('DATABASE_URL')
            ch = DBcon.DataConnect(db_url)
        except:
            db_url = config.DATABASE_URL
            ch = DBcon.DataConnect(db_url)
        self.text = text
        self.ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
        self.cut_text = self.ama.word_tokenize(text)
        self.wtp = dict((x, y) for x, y in ch.word_type())
        ch.close_con()

    # สร้าง dict ที่คำเป็น key ส่วนชนิด เป็น value
    def tran_type(self):
        dic_s = self.wtp
        all_word = dic_s.keys()
        new_list = []
        for word in self.cut_text:
            if word in all_word:
                new_list.append({word: dic_s[word]})
            else:
                new_list.append({word: 0})
        return new_list

    # สร้าง dict ที่ชนิดเป็น key ส่วนลำดับของคำชนิดเดียวที่พบติดกันเป็น value
    def madas(self):
        pana = self.tran_type()
        anan = self.cut_text
        bove = []
        for e, mam in enumerate(pana):
            n = 1
            if e == 0:
                bove.append({pana[e][anan[e]]: n})
            elif pana[e][anan[e]] == pana[e-1][anan[e-1]]:
                bove.append({pana[e][anan[e]]: bove[-1][pana[e][anan[e]]]+1})
            else:
                bove.append({pana[e][anan[e]]: n})
        return bove

    # นำคำกริยาที่อยู่ติดกันมาเรียงกัน
    def yul(self):
        pang = self.madas()
        anan = self.cut_text
        doo = self.tran_type()
        maju = []
        for n, man in enumerate(doo):
            if man[anan[n]] == 2:
                s = pang[n][2]
                rebu = []
                while s > 0:
                    rebu.append(anan[n+1-s])
                    s = s - 1
                maju.append("".join(rebu))
            else:
                pass
        return maju

    # คำนามคำแรกที่พบในประโยค
    def first_nam(self):
        anan = self.cut_text
        doo = self.tran_type()
        maju = []
        for n, man in enumerate(doo):
            if man[anan[n]] == 1:
                maju.append(anan[n])
            elif man[anan[n]] == 2:
                break
            else:
                pass
        return maju

    def sd(self):
        type_num = [y for x, y in all_bind]
        if 1 in type_num:
            if 2 in type_num:
                if type_num.index(2) > type_num.index(1):
                    pass

text = 'ผู้บัญชาการตำรวจภาค 8 สั่งย้ายตำรวจทั้ง 3 นาย ที่ถูกกล่าวหาว่าข่มขู่เรียกรับเงินชาวบ้าน เพื่อแลกกับการไม่ให้ถูกจับกุม กรณีซื้อขายลูกหอยแครง #ThaiPBS #ทันข่าวเด่น'
dfa = AnText(text)
ea = dfa.tran_type()
dr = dfa.madas()
aa = dfa.yul()
tt = dfa.first_nam()
usi = dfa.cut_text
print(text)
print(str(ea))
print(dr)
print(aa)
print(tt)
print(usi)




