import datetime
import sys

###    0 1 2 3 4 5 6 7 8 9 A B 0 1 2 3 4 5 6 7 8 9 A B "
#   = "110011001100110011001100110011001100110011001100"
S1  = "                              FFFFFFFFFFFFFFFF  " # 3 - 11
S2  = "                         FFFFFFFFFFFFFFFFFFFFF  " # 12- 11

S3  = "                              FFFFFFFFFFFFFFF   " # 3 - 10:30
S4  = "                               FFFFFFFFFFFFFFF  " # 3:30 - 11
S5  = "                         FFFFFFFFFFFFFFFFFFFF   " # 12- 10:30
S6  = "                          FFFFFFFFFFFFFFFFFFFF  " # 12:30- 11



class Timer():
    def __init__(self):
        self.schedule=[S1, S1, S1, S1, S1, S2, S2]  # Mon to Sun

    def set(self, mon=S1, tue=S1, wed=S1, thu=S1, fri=S1, sat=S2, sun=S2):
        self.schedule=[mon, tue, wed, thu, fri, sat, sun]  # Mon to Sun

    def on(self):
        return self.state()

    def off(self):
        return  not self.state()

    def state(self):
        now = datetime.datetime.now()
        index = now.weekday() # return 0 - 7 (0=monday)
        s = self.schedule[index]
        m = now.minute % 30
        z = now.hour*2 + (now.minute/30)
        q = s[z]
        print z,q
        if q != " " and q != "0":
            try:
                i = int(q,16)
                print i,m
                if m < 8:
                    return i & 1 > 0
                if m>7 and m < 15:
                    return i & 2 > 0
                if m>14 and m < 23:
                    return i & 4 > 0
                if m>22:
                    return i & 8 > 0

            except ValueError:
                return False

        return False
