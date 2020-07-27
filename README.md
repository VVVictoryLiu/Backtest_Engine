# EngineForStock
事件驱动型量化引擎，python3.x和pandas1.x版本以上稳定运行

## mac.py

定义了量化策略类(该类继承于strategy类，重写了其中的主要方法），实现了基于长短窗口的简单均线策略，效果很一般，仅用来测试代码可用性

## indicators_stratgy.py

基于SAR买卖指标的量化策略，SAR指标的计算方法见tech_indicators仓库，在回测中取得了惊人的效果

## backtest.py

回测引擎的核心类，基于DataHandle类返回的bar数据和events列表处理交易信号，在protfolio类中实现仓位调整

## data.py

从本地或接口中获取全部股票信息，封装为可迭代类型，通过update_bars()方法返回最新一日bar数据
