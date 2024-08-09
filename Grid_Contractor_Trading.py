import time
import okex.Account_api as Account
import okex.Funding_api as Funding
import okex.Market_api as Market
import okex.Public_api as Public
import okex.Trade_api as Trade
import okex.subAccount_api as SubAccount
import json
import time
import pandas as pd
import os
import okx.MarketData as MarketData


def get_market_price(ccy="ETH"):
    ccy = ccy + "-USDT"
    _result = marketAPI.get_ticker(ccy)
    return float(_result['data'][0]['last'])


def get_contract_price(ccy="ETH"):
    ccy = ccy + "-USDT-SWAP"
    _result = marketAPI.get_ticker(ccy)
    return float(_result['data'][0]['last'])


def analyze_trading_price(_now_price, _coefficient, ):
    upper_price = []
    lower_price = []
    tem_price = _now_price
    _fix = _now_price * _coefficient / 2
    for i in range(40):
        tem_price = tem_price * (1 + _coefficient / 2) + _fix
        upper_price.append(tem_price)
    tem_price = _now_price
    for i in range(40):
        tem_price = tem_price * (1 - _coefficient / 2) - _fix
        lower_price.append(tem_price)
    lower_price.reverse()
    __now_price = [_now_price]
    full_price = lower_price + __now_price + upper_price
    return full_price


def place_order(_price, ccy="ETH", _side="buy", _volume=0.1):
    ccy = ccy + "-USDT-SWAP"
    __result = tradeAPI.place_order(
        instId="ETH-USDT-SWAP",
        tdMode="cross",
        side=_side,
        ordType="limit",
        px=_price,
        sz=_volume  # contractor number
    )
    print(__result)
    return __result


# def get_exposure(ccy="ETH-USDT-SWAP"):
#     result = accountAPI.get_position_risk('SWAP')
#     for i in result['data']:
#


def grid_strategy(_ccy="ETH"):
    _excel_filename = ccy+"-parameters_and_prices_with_bool.xlsx"
    _df = pd.read_excel(_excel_filename, sheet_name='Sheet1')
    upper_price = 0
    lower_price = 0
    upper_index = 0
    lower_index = 0
    now_index = 0
    try_count = 0
    for i in range(6, 87):
        if _df.iloc[i, 1] == 2:
            now_index = i
            upper_price = _df.iloc[i+1, 0]
            upper_index = i+1
            lower_price = _df.iloc[i-1, 0]
            lower_index = i-1
            if _df.iloc[upper_index, 1] != 1:
                place_order(ccy=_ccy, _price=upper_price, _side="sell")
                _df.iloc[upper_index, 1] = 1
            if _df.iloc[lower_index, 1] != 1:
                place_order(ccy=_ccy, _price=lower_price, _side="buy")
                _df.iloc[lower_index, 1] = 1
            _df.to_excel(_excel_filename, index=False)
            break
    _now_price = get_contract_price(_ccy)
    print(_now_price)
    max_try_count = _df.iloc[0, 1]
    while True:
        try:
            _now_price = get_contract_price(_ccy)
            if _now_price >= upper_price:
                print(f"sell order fulfilled at price {_now_price}")
                now_index = now_index + 1
                upper_index = now_index + 1
                lower_index = now_index - 1
                upper_price = _df.iloc[upper_index, 0]
                lower_price = _df.iloc[lower_index, 0]
                print(upper_price)
                print(lower_price)
                if _df.iloc[upper_index, 1] != 1:
                    place_order(ccy=_ccy, _price=upper_price, _side="sell")
                    _df.iloc[upper_index, 1] = 1
                if _df.iloc[lower_index, 1] != 1:
                    place_order(ccy=_ccy, _price=lower_price, _side="buy")
                    _df.iloc[lower_index, 1] = 1
                _df.iloc[now_index, 1] = 2
                # sell
                _df.to_excel(_excel_filename, index=False)
                print("sell data updated")
                time.sleep(0.5)
            if _now_price <= lower_price:
                print(f"buy order fulfilled at price {_now_price}")
                now_index = now_index - 1
                upper_index = now_index + 1
                lower_index = now_index - 1
                upper_price = _df.iloc[upper_index, 0]
                lower_price = _df.iloc[lower_index, 0]
                print(upper_price)
                print(lower_price)
                if _df.iloc[upper_index, 1] != 1:
                    place_order(ccy=_ccy, _price=upper_price, _side="sell")
                    _df.iloc[upper_index, 1] = 1
                if _df.iloc[lower_index, 1] != 1:
                    place_order(ccy=_ccy, _price=lower_price, _side="buy")
                    _df.iloc[lower_index, 1] = 1
                _df.iloc[now_index, 1] = 2
                _df.to_excel(_excel_filename, index=False)
                print("buy data updated")
                time.sleep(0.5)

            time.sleep(0.3)
        except Exception as e:
            print(e)
            try_count += 1
            if try_count >= max_try_count:
                print('error, system terminated.')
                exit()
            else:
                continue


if __name__ == '__main__':
    api_key = "c15acbfa-e015-4547-b05b-51cd77514f15"
    secret_key = "528DA648FA63D015792CE35E84B464C7"
    passphrase = "faLL2012$"

    ccy = "ETH"

    flag = '0'  # 实盘 real trading
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

    filename = ccy+'-parameters_and_prices_with_bool.xlsx'
    current_path = os.getcwd()
    file_path = os.path.join(current_path, filename)

    if not (os.path.isfile(file_path)):
        # initializing
        now_price = get_contract_price(ccy)
        parameters_list = ["Max_trying_count", "buy_order_volume", "sell_order_volume", "now_volume"]
        price_list = analyze_trading_price(now_price, 0.01)
        parameters_value = [1000, 0.1, 0.1, now_price]

        parameters_df = pd.DataFrame({
            'Parameter': parameters_list,
            'Value': parameters_value
        })

        price_df = pd.DataFrame({
            'Price': price_list
        })
        price_df['IsAboveThreshold'] = 0

        with pd.ExcelWriter(filename) as writer:
            parameters_df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=0)
            price_df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=len(parameters_list) + 2)

        print("Excel created.")
        df = pd.read_excel(filename, sheet_name='Sheet1')
        df.iloc[46, 1] = 2  # center price
        df.to_excel(filename, index=False)

    api_key = "c15acbfa-e015-4547-b05b-51cd77514f15"
    secret_key = "528DA648FA63D015792CE35E84B464C7"
    passphrase = "faLL2012$"

    flag = '0'  # real trading
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

    currency_contract = ccy+"-USDT-SWAP"
    accountAPI.set_leverage(
        instId=currency_contract,
        lever="1",
        mgnMode="cross"
    )
    accountAPI.set_leverage(
        instId=currency_contract,
        lever="1",
        mgnMode="isolated"
    )
    accountAPI.set_leverage(
        instId=currency_contract,
        lever="1",
        posSide="long",
        mgnMode="isolated"
    )

    grid_strategy(ccy)
