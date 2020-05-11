from backtest import trader
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', help='stock name i.e. MSFT')
    parser.add_argument('--reuse', type=bool, default=False)
    args = parser.parse_args()
    print(parser)
    print(args)
    trader.run(args.symbol, reuse_data=args.reuse)