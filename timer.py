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

S10 = "F       F       F       F       F       F       "  # every 4 hours
ST = "5555555555555555555555555555555555555555555555555"


class Timer():
    def __init__(self, name="timer"):
        self.schedule = None
        self.name = name

    def set(self, mon=S1, tue=S1, wed=S1, thu=S1, fri=S1, sat=S2, sun=S2):
        self.schedule=[mon, tue, wed, thu, fri, sat, sun]  # Mon to Sun
        self.current = self.calc_state()
        self.next_change = self.calc_next_change()

    def on(self):
        return self.state()

    def off(self):
        return  not self.state()

    def state(self):
        if self.schedule is None:
            return "No schedule"
        new_state = self.calc_state()
        if new_state != self.current:
            self.next_change = self.calc_next_change()
            self.current = new_state
        return self.current

    def calc_next_change(self):
        now = datetime.datetime.now()
        while True:
            now += datetime.timedelta(minutes=1)
            new_state = self.calc_state(now)
            if new_state != self.current:
                return "{h:02}:{m:02}".format(h=now.hour, m=now.minute)
        return "??"

    def calc_state(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        index = now.weekday() # return 0 - 7 (0=monday)
        s = self.schedule[index]
        m = now.minute % 30
        z = now.hour*2 + (now.minute/30)
        q = s[z]
        if q != " " and q != "0":
            try:
                i = int(q,16)
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


