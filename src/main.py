from pprint import pformat, pprint
from src.strategy import strategy
import sys
from .game import Game
import logging

def main():
    g = Game()
    while (s := input()).__contains__("settings"):
        g.add_setting(s)
    while True:  # Runs the main loop
        try:
            s = input()
        except:  # TODO: Be spectific. i.e. EOFError:
            break
        if s.__contains__("update game stacks"):
            g.portfolio.update(s)
        elif s.__contains__("update game next_candles"):
            g.add_candles(s)
        else:
            strategy(g)