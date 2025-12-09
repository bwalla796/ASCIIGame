import curses
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.max_health = 10
        self.weapon = 5
        self.armor = 0
        self.monsters_slain = 0
        self.abilities = []

    def undraw(self, scr):
        scr.addstr(self.y - 1, self.x, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x + 1, " ", curses.color_pair(1))
        scr.addstr(self.y, self.x - 1, " ", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x - 1, " ", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x + 1, " ", curses.color_pair(1))

    def draw(self, scr):
        scr.addstr(self.y - 1, self.x, "8", curses.color_pair(1))
        scr.addstr(self.y, self.x, "@", curses.color_pair(1))
        scr.addstr(self.y, self.x + 1, "-", curses.color_pair(1))
        scr.addstr(self.y, self.x - 1, "-", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x - 1, "/", curses.color_pair(1))
        scr.addstr(self.y + 1, self.x + 1, "\\", curses.color_pair(1))

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
           
    def addAbility(self, ability):
        self.abilities.append(ability)       
        