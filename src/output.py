class outbuf:
    def __init__(self):
        self.buf: str = ""
        self.printed: str = ""

    def add(self, s):
        self.buf += s

    def clear(self):
        self.buf = ""

    def out(self):
        self.printed += self.buf + "\n"
        print(self.buf)
        self.clear()

    def printclear(self):
        self.printed = ""
