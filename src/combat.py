from helpers import print_menu
from classes.player import Player
from classes.round import Round
from classes.monster import Monster
from collections import Counter
import curses

def handleCombat(scr, player, monster, stage):
    player.draw(scr)
    player.renderHealthCounter(scr)
    monster.draw(scr)
    monster.renderHealthCounter(scr)
    while monster.health > 0 and player.health > 0:
        attack_choice = display_combat_menu(scr, False, player.abilities)
        display_combat_menu(scr, True)
        if attack_choice == "Attack":
            monster.health = monster.health - (player.weapon - monster.armor if player.weapon - monster.armor > 0 else 0)
        elif attack_choice == "Fireball":
            monster.health = monster.health - (25 - monster.armor if player.weapon - monster.armor > 0 else 0)    
        elif attack_choice == "Defend":
            player.armor *= 2
        elif attack_choice == "Acid Splash":
            monster.health = monster.health - (player.weapon // 2) 
        elif attack_choice == "Poison Gas": 
            monster.health = monster.health - ((player.weapon // 5) - monster.armor if (player.weapon // 5) - monster.armor > 0 else 0) 
            monster.add_condition("Poisoned")     

        if monster.health > 0:
            conditions_counts = Counter(monster.conditions)
            #Todo: need to turn conditions into a list of objects that contains the duration of the condition
            monster.health = monster.health - conditions_counts["Poisoned"]
            player.health = player.health - (monster.weapon - player.armor if monster.weapon - player.armor > 0 else 0)
            if attack_choice == "Defend":
                player.armor //= 2
            if player.health > 0:
                player.renderHealthCounter(scr)
                monster.renderHealthCounter(scr)
                scr.refresh() 



def display_combat_menu(stdscr, destroy=False, abilities=[]):
    options = ["Attack", "Defend"] + abilities
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