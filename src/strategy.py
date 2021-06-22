from typing import List
import datetime
from .game import Game
import sys
import statistics

TAKE_PROFIT_VALUE = 1.05

def buy(g: Game):
    ammount_owned = g.portfolio.portfolio['USDT']
    current_close: float = g.candles['USDT_BTC'][-1].close
    ammount: float = g.portfolio.portfolio['USDT'] / current_close * ((100 - g.settings.transaction_fee_percent) / 100)
    if (g.portfolio.portfolio['USDT'] > 100):
        print(f"buying at ${current_close} for {ammount} and updating stats", file=sys.stderr)
        g.stats.lastbuy_value = ammount_owned
        print(f"buy USDT_BTC {ammount:.3f}")
    else:
        print(f"Couldnt buy at ${current_close} because not enough USDT", file=sys.stderr)
        print('no_moves')

def maybesell(g: Game):
    ammount_owned = g.portfolio.portfolio['BTC']
    current_close: float = g.candles['USDT_BTC'][-1].close
    ammount: float = ammount_owned * ((100 - g.settings.transaction_fee_percent) / 100)
    value = ammount * current_close
    if (value > g.stats.lastbuy_value * TAKE_PROFIT_VALUE):
        print(f"Selling at ${current_close:.3f} for {value:.3f}", file=sys.stderr)
        print(f"sell USDT_BTC {ammount:.3f}")
    else:
        print('no_moves')


def bb(sma, period):
    std = statistics.stdev((o.close for o in period))
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb


def sma(period):
    mean = statistics.mean((o.close for o in period))
    return mean

def strategy(g: Game):
    if ('USDT_BTC' in g.candles):
        period = g.candles['USDT_BTC'][-20:]
        # l = list(o.close for o in period)
        # print(l, file=sys.stderr)
        ma = sma(period)
        high, low = bb(ma, period)
        # print(f'Sma : {ma}\t Bb: {low, high}, Last close: {period[-1].close}, outside BB ? {"---- YES!!!" if (period[-1].close < low or period[-1].close > high) else "NO" }', file=sys.stderr)
        if period[-1].close < low or period[-1].close > high:
            if period[-1].close < low:
                buy(g)
            else:
                print("no_moves")
        else:
            maybesell(g)


# UPPER_BB = STOCK SMA + SMA STANDARD DEVIATION * 2
# LOWER_BB = STOCK SMA - SMA STANDARD DEVIATION * 2
# IF PREV_STOCK > PREV_LOWERBB & CUR_STOCK < CUR_LOWER_BB => BUY
# IF PREV_STOCK < PREV_UPPERBB & CUR_STOCK > CUR_UPPER_BB => SELL