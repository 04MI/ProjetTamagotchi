NORMAL = 'normal'
HIDDEN = 'hidden'

class PhotoImage():
    def __init__(self, file=""):
        self.file = file
        self.x = -1
        self.y = -1
        self.anchor = None
        self.state = None

        self.w = 10
        self.h = 10

    
    def width(self):
        return self.w

    def height(self):
        return self.h


class messagebox():
    def __init__(self) -> None:
        pass

class Tree():
    def __init__(self) -> None:
        pass