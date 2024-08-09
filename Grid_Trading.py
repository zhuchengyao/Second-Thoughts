import time
import okex.Account_api as Account
import okex.Funding_api as Funding
import okex.Market_api as Market
import okex.Public_api as Public
import okex.Trade_api as Trade
import okex.subAccount_api as SubAccount
import okex.status_api as Status
import json
import time
import okx.MarketData as MarketData


def get_ETH_contract_price(ccy="ETH"):
    ccy = ccy+"-USDT-SWAP"
    _result = marketAPI.get_ticker(ccy)


def get_market_price(ccy="BTC"):
    ccy = ccy+"-USDT"
    _result = marketAPI.get_ticker(ccy)
    return float(_result['data'][0]['last'])


def calculate_upper_price(__now_price, coefficient, fix):
    _1_upper_price = __now_price*(1 + coefficient/2) + fix
    _2_upper_price = _1_upper_price * (1+coefficient/2) + fix
    return _1_upper_price, _2_upper_price


def calculate_lower_price(__now_price, coefficient, fix):
    _1_lower_price = __now_price*(1 - coefficient/2) - fix
    _2_lower_price = _1_lower_price * (1 - coefficient/2) - fix
    return _1_lower_price, _2_lower_price


def grid_strategy(ccy="BTC", coefficient=0.008):
    _now_price = get_market_price(ccy)
    print(_now_price)
    _1_upper_price = _now_price * (1 + coefficient)
    _1_lower_price = _now_price * (1 - coefficient)
    print(_1_lower_price)
    print(_1_upper_price)
    fix = coefficient * _now_price/2
    try_count = 0
    max_try_count = 300
    while True:
        try:
            _now_price = get_market_price(ccy)
            if _now_price >= _1_upper_price:
                # sell
                volumn = 0.0029
                place_order("sell", volumn)
                print(f"sell order complete. price at {_1_upper_price}")
                _1_lower_price, _2_lower_price = calculate_lower_price(_1_upper_price, coefficient, fix)
                _1_upper_price, _2_upper_price = calculate_upper_price(_1_upper_price, coefficient, fix)
                print(_1_upper_price)
                print(_1_lower_price)
                time.sleep(0.2)
            elif _now_price <= _1_lower_price:
                volumn = 0.003*_now_price
                place_order("buy", volumn)
                print(f"buy order complete. price at {_1_lower_price}")
                _1_upper_price, _2_upper_price = calculate_upper_price(_1_lower_price, coefficient, fix)
                _1_lower_price, _2_lower_price = calculate_lower_price(_1_lower_price, coefficient, fix)
                print(_1_upper_price)
                print(_1_lower_price)
                time.sleep(0.2)
            else:
                # print("now price is: ")
                # print(_now_price)
                # print("\n")
                time.sleep(0.5)
                continue
        except Exception as e:
            print(e)
            try_count += 1
            if try_count >= max_try_count:
                print('error, system terminated.')
                exit()
            else:
                continue


def place_limit_order(side="sell", _volume=0.01, _price=3000):
    result = tradeAPI.place_order(
        instId="ETH-USDT",
        tdMode="cash",
        side=side,
        ordType="limit",
        px=_price,
        sz=_volume
        )
    print(result)


def place_order(side="sell", _volumn=0.01):
    result = tradeAPI.place_order(
        instId="ETH-USDT",
        tdMode="cash",
        side=side,
        ordType="market",
        sz=_volumn
        )
    print(result)


if __name__ == '__main__':


    flag = '0'  # 实盘 real trading
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)

    # result = accountAPI.get_max_withdrawal('USDT')
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)

    # result = fundingAPI.get_balances('USDT')
    marketDataAPI = MarketData.MarketAPI(flag=flag)

    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

    # grid_strategy("ETH")
    grid_strategy("ETH")
