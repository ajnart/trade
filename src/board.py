import logging

# from src.game import Game
from pprint import pformat


class Candle(object):
    date = 0.0
    high = 0.0
    low = 0.0
    open = 0.0
    close = 0.0
    volume = 0.0
    left = ""
    right = ""


class Board(object):
    candles: dict[str, list[Candle]] = {}

    def add_candles(self, g, str: str):
        if "update game next_candles " in str:
            str = str.replace("update game next_candles ", "")

        self.add_candle(str.split(";"), g)

    def add_candle(self, candles: list, g):
        for candle in candles:
            infos = candle.split(",")
            added = Candle()
            added.left, added.right = infos[g.format["pair"]].split("_")
            added.close = float(infos[g.format["close"]])
            added.open = float(infos[g.format["open"]])
            added.volume = float(infos[g.format["volume"]])
            added.high = float(infos[g.format["high"]])
            added.low = float(infos[g.format["low"]])
            added.date = infos[g.format["date"]]
        if (infos[g.format["pair"]] in self.candles):
            self.candles[infos[g.format["pair"]]].append(added)
        else:
            list = []
            list.append(added)
            pair = infos[g.format["pair"]]
            self.candles[pair] = [list]
            # Ask the format for the position of the pair info and append it to the list of candles on the board