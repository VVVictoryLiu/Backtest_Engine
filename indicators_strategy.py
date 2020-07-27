import datetime
import numpy as np

from backtest import Backtest
from data import Historic_SQL_DataHandler
from event import SignalEvent
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from strategy import Strategy


class MACD_SAR_Strategy(Strategy):
    """
    基于MACD和SAR买卖信号的交易策略
    """

    def __init__(self, bars, events, window=5):
        """
        初始化策略，bars参数直接传入backtest中实例化的Datahandle类，events为执行的事件
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.window = window
        self.count =0


        # Set to True if a symbol is in the market
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        初始空仓所有股票，设置标志为‘out’
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = 'OUT'
        return bought

    def calculate_signals(self, event):
        """

        """
        self.count = self.count+1
        if event.type == 'MARKET':
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars_values(symbol, "open", N=2)
                bars_sar = self.bars.get_latest_bars_values(symbol, "sar_trigger", N=1)
                #bars_macd = self.bars.get_latest_bars_values(symbol, "macd_trigger", N=self.window)

                if bars.size>0:
                    buy_sar = len([x for x in bars_sar if x=='buy'])
                    #buy_macd = len([x for x in bars_macd if x=='buy'])

                    #sale_macd = len([x for x in bars_macd if x == 'sale'])
                    sale_sar = len([x for x in bars_sar if x == 'sale'])

                    dt = self.bars.get_latest_bar_datetime(symbol)
                    sig_dir = ""
                    strength = 1.0
                    strategy_id = 1

                    if buy_sar>0 and self.bought[symbol] == "OUT":
                        print(str(dt)[:10],'_buy','%.2f'%(bars[-1]),symbol)
                        sig_dir = 'LONG'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'LONG'

                    elif sale_sar>0 and self.bought[symbol] == "LONG":
                        print(str(dt)[:10],'sale','%.2f'%(bars[-1]),symbol)
                        sig_dir = 'EXIT'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'OUT'



if __name__ == "__main__":
    database_path = "mysql+pymysql://root@127.0.0.1:3306/stock_base"
    symbol_list = ['sz.000001']
    initial_capital = 100000.0
    start_date = datetime.datetime(2014, 1, 1, 0, 0, 0)
    heartbeat = 0.0

    backtest = Backtest(database_path,
                        symbol_list,
                        initial_capital,
                        heartbeat,
                        start_date,
                        Historic_SQL_DataHandler,
                        SimulatedExecutionHandler,
                        Portfolio,
                        MACD_SAR_Strategy)

    backtest.simulate_trading()

