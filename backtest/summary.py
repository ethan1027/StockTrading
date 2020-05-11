import backtrader as bt
class Summary:
    def __init__(self, cerebro: bt.Cerebro, strategy: bt.Strategy, run_strat, data, metadata):
        self.cerebro = cerebro
        self.strategy = strategy
        self.run_strat = run_strat
        self.data = data
        self.metadata = metadata

    def slow(self, slow):
        self.slow = slow
        return self

    def fast(self, fast):
        self.fast = fast
        return self

    def get_brokerval(self):
        return self.cerebro.getbroker().getvalue()

    def __str__(self):
        broker_value = self.get_brokerval()
        name = self.strategy.__name__
        time_drawdown = self.run_strat.analyzers.time_drawdown.get_analysis()
        maxdrawdown = time_drawdown['maxdrawdown']
        maxdrawdownperiod = time_drawdown['maxdrawdownperiod']
        try:
            interval = self.metadata['4. Interval']
        except:
            interval = 'daily'
        s = f'val: {broker_value}, s: {name} {self.fast} {self.slow}, int: {interval}, mdd: {maxdrawdown}, mddp: {maxdrawdownperiod}'
        return s
