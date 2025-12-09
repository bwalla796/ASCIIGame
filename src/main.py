import curses
import math
from classes.player import Player
from classes.monster import Monster
from classes.round import Round
from curses import wrapper
from combat import display_combat_menu, handleCombat
from helpers import print_menu

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    menu_options = ['New Game', 'Quit']
    current_row_idx = 0

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    while True:
        print_menu(stdscr, current_row_idx, menu_options, start_y=10)
        
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu_options) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            return menu_options[current_row_idx] 
        elif key == ord('q'):
            return "Quit"

def display_shop_menu(stdscr, destroy=False, abilities=False):
    if not abilities:
        options = ["+Weapon", "+Armor", "+Health", "Pass"]
    else:
        options = ["Fireball", "Poison Gas", "Acid Splash", "Pass"]
    selected_index = 0
    
    MAX_Y, MAX_X = stdscr.getmaxyx()
    menu_y = MAX_Y - 6
    menu_x = 4

    stdscr.move(menu_y, menu_x)
    for _ in range(len(options) + 2):
        stdscr.clrtoeol()

    if not destroy:
        while True:
            for i, option in enumerate(options):
                display_str = f"> {option}" if i == selected_index else f"  {option}"

                if i == selected_index:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(menu_y + i, menu_x, display_str)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(menu_y + i, menu_x, display_str)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
            elif key == curses.KEY_DOWN and selected_index < len(options) - 1:
                selected_index += 1
            elif key in [curses.KEY_ENTER, 10, 13]: 
                return options[selected_index]                 

def main(stdscr):
    print("Hello from asciigame!")
    stdscr.timeout(300)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    MAX_Y, MAX_X = stdscr.getmaxyx()
    main_menu_selected = main_menu(stdscr)
    if main_menu_selected == "Quit":
        curses.nocbreak
        stdscr.keypad(False)
        curses.echo()

        curses.endwin
        return

    if(curses.has_colors()):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE
        , curses.COLOR_BLACK)
    else:
        curses.init_pair(1, 0, 1)
        
    current_pos_x = 8
    current_pos_y = MAX_Y - 8

    stdscr.addstr(current_pos_y, current_pos_x, "@", curses.color_pair(1))
    stdscr.refresh()

    curses.curs_set(0)
    player = Player(current_pos_x, current_pos_y)
    player.draw(stdscr)

    mon_health = 10
    mon_armor = 0
    mon_weapon = 3
    monster = Monster(MAX_X - 8, current_pos_y, mon_health, mon_weapon, mon_armor)    

    stage = Round(1)

    while True:
        c = stdscr.getch()
        
        if (stage.round_int % 5 == 0) :
            stdscr.addstr(4, MAX_X // 2 - len("Project David") // 2, "Goliath appears...", curses.A_BOLD)

        player.undraw(stdscr)
        player.draw(stdscr)
        monsters_count = 1
        if monster is not None:
            handleCombat(stdscr, player, monster, stage)
            if player.health > 0:
                monster = None
            else:
                break  
        else:
            is_boss_round = stage.round_int % 5 == 0
            selected_in_shop = display_shop_menu(stdscr, False, is_boss_round)
            if is_boss_round:
                #Todo: Add upgrades to abilities upon repeat selection
                if selected_in_shop != "Pass":
                    player.addAbility(selected_in_shop)
            else:    
                if selected_in_shop == "+Weapon":
                    player.improve_weapon()
                elif selected_in_shop == "+Armor":
                    player.improve_armor()
                elif selected_in_shop == "+Health":
                    player.improve_health()
            player.health = player.max_health    
            stage.next()
            mon_health += 10 
            mon_armor += 2
            mon_weapon += 2
            if (stage.round_int % 5 == 0):
                mon_weapon += 2
                mon_health *= 2
            
            monster = Monster(MAX_X - 8, current_pos_y, mon_health, mon_weapon, mon_armor)       
        
        stdscr.clear() 
        stdscr.refresh()

        if(c == ord('p')):
            break
        elif c == ord('q'):
            break

    curses.nocbreak
    stdscr.keypad(False)
    curses.echo()

    curses.endwin


if __name__ == "__main__":
    wrapper(main)
