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


if __name__ == '__main__':


    flag = '0'  # 实盘 real trading
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)

    # result = accountAPI.get_max_withdrawal('USDT')
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)

    # result = fundingAPI.get_balances('USDT')

    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
    accountAPI.set_leverage(
        instId="ETH-USDT-SWAP",
        lever="1",
        mgnMode="cross"
    )
    accountAPI.set_leverage(
        instId="ETH-USDT-SWAP",
        lever="1",
        mgnMode="isolated"
    )
    accountAPI.set_leverage(
        instId="ETH-USDT-SWAP",
        lever="1",
        posSide="long",
        mgnMode="isolated"
    )

    result = tradeAPI.place_order(
        instId="ETH-USDT-SWAP",
        tdMode="cross",
        side="buy",
        ordType="limit",
        px=3000,
        sz="0.1"  # contractor number
    )
    print(result)

    if result["code"] == "0":
        print("Successful order request，order_id = ", result["data"][0]["ordId"])
    else:
        print("Unsuccessful order request，error_code = ", result["data"][0]["sCode"], ", Error_message = ",
              result["data"][0]["sMsg"])

    print(result)

