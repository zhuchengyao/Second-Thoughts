import time

from pip._internal.utils.misc import enum

import okex.Account_api as Account
import okex.Funding_api as Funding
import okex.Market_api as Market
import okex.Public_api as Public
import okex.Trade_api as Trade
import okex.subAccount_api as SubAccount
import okex.status_api as Status
import json
import time

def get_ETH_contract_price():
    _result = marketDataAPI.get_tickers(instType="SWAP")
    return float(_result['data'][37]['last'])



if __name__ == '__main__':
    api_key = "c15acbfa-e015-4547-b05b-51cd77514f15"
    secret_key = "528DA648FA63D015792CE35E84B464C7"
    passphrase = "faLL2012$"

    flag = '0'  # 实盘 real trading
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)

    # result = accountAPI.get_max_withdrawal('USDT')
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)

    # result = fundingAPI.get_balances('USDT')

    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    import okx.PublicData as PublicData

    import okx.MarketData as MarketData

    flag = "1"  # live trading: 0, demo trading: 1

    marketDataAPI = MarketData.MarketAPI(flag=flag)
    result = marketDataAPI.get_ticker("ETH-USDT-SWAP")

    print(result)

