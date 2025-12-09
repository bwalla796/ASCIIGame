import curses
class Monster():
    def __init__(self, x, y, max_health, weapon, armor):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = self.max_health
        self.weapon = 3
        self.armor = 0
        self.conditions = []

    def undraw(self, scr):
        scr.addstr(self.y - 1, self.x, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x + 1, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x - 1, " ", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x - 1, " ", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x + 1, " ", curses.color_pair(1))

    def draw(self, scr):
        scr.addstr(self.y - 1, self.x, "%", curses.color_pair(2))
        scr.addstr(self.y, self.x, "G", curses.color_pair(2))
        scr.addstr(self.y, self.x + 1, "r", curses.color_pair(2))
        scr.addstr(self.y, self.x - 1, "~~", curses.color_pair(2))
        scr.addstr(self.y + 1, self.x - 1, "?", curses.color_pair(2))
        scr.addstr(self.y + 1, self.x + 1, "?", curses.color_pair(2))

    def renderHealthCounter(self, scr):
        scr.addstr(4, self.x - 1, "               ", curses.color_pair(3))
        scr.refresh()   
        scr.addstr(4, self.x - 1, f"{self.health}/{self.max_health}", curses.color_pair(3))    

    def improve_armor(self):
        self.armor += 1
    def improve_weapon(self):
        self.weapon += 1
    def improve_health(self):
        self.max_health += 5
        self.health = self.max_health   

    def add_condition(self, condition):
        self.conditions.append(condition)             
           
        