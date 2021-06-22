import sys
from typing import Dict, List
class Game:
    class Stats:
        profit: float = 0.0
        lastbuy_value: float = 0.0
    #Class settings
    class Settings:
        transaction_fee_percent: float = 0.0
        candle_interval: float = 0.0
        candles_given: float = 0.0
        candles_total: float = 0.0
        initial_stack: float = 0.0
        time_per_move: float = 0.0
        timebank: float = 0.0

    # Class candle
    class Candle(object):
        date: float = 0.0
        high: float = 0.0
        low: float = 0.0
        open: float = 0.0
        close: float = 0.0
        volume: float = 0.0
        left = ""
        right = ""

    def add_candles(self, str: str):
        if "update game next_candles " in str:
            str = str.replace("update game next_candles ", "")
        self.add_candle(str.split(";"))

    def add_candle(self, s):
        for candle in s:
            infos = candle.split(",")
            added = self.Candle()
            added.left, added.right = infos[self.format["pair"]].split("_")
            added.close = float(infos[self.format["close"]])
            added.open = float(infos[self.format["open"]])
            added.volume = float(infos[self.format["volume"]])
            added.high = float(infos[self.format["high"]])
            added.low = float(infos[self.format["low"]])
            added.date = float(infos[self.format["date"]])
        
        if (infos[self.format["pair"]] in self.candles):
            self.candles[infos[self.format["pair"]]].append(added)
        else:
            list = []
            list.append(added)
            pair = infos[self.format["pair"]]
            self.candles[pair] = list

    #Class portfolio
    class Portfolio:
        portfolio: Dict[str, float] = dict()

        def __repr__(self) -> str:
            return "\n".join(
                f"{coin}:{ammount}" for coin, ammount in self.portfolio.items()
            )

        def update(self, str: str):
            str = str.replace("update game stacks ", "")
            coins = str.split(",")
            for item in coins:
                coin, value = item.split(":")
                self.portfolio[coin] = float(value)
            # print(f"Updated stacks: {self.portfolio}", file=sys.stderr)



    portfolio = Portfolio()
    stats = Stats()
    settings = Settings()
    candles: Dict[str, List[Candle]] = dict()
    # pair
    # close
    # open
    # volume
    # high
    # low
    # date
    format: dict[str, int] = dict()

    # Add setting method
    def add_setting(self, orig: str):         
        s = orig.split()
        try:
            if "candle_interval" in s:
                self.settings.candle_interval = float(s[2])
            elif "candles_given" in s:
                self.settings.candles_given = float(s[2])
            elif "candles_total" in s:
                self.settings.candles_total = float(s[2])
            elif "initial_stack" in s:
                self.settings.initial_stack = float(s[2])
            elif "time_per_move" in s:
                self.settings.time_per_move = float(s[2])
            elif "timebank" in s:
                self.settings.timebank = float(s[2])
            elif "transaction_fee_percent" in s:
                self.settings.transaction_fee_percent = float(s[2])
            elif "candle_format" in s:
                orig = orig.replace("settings candle_format ", "")
                idx = 0
                for i in orig.split(","):
                    self.format[i] = idx
                    idx += 1
        except Exception as e:
            print(f"Error: {e}, string: {orig}", file=sys.stderr)
            print('Crash: Settings fucked up', file=sys.stderr)
            exit(84)

