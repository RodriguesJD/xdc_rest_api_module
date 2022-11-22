import requests
from pprint import pprint
import json


def blockscan_response(url):
    response = requests.get(url=f"{url}")
    print(response.json()["items"][0].keys())
    # print(url)
    # print(response.status_code)
    # headers = response.headers
    # print(f"total: {response.json()['total']}")
    # print(f"perpage:{response.json()['perPage']}")
    # print(f"currentpage: {response.json()['currentPage']}")
    # print(f"pages: {response.json()['pages']}")
    # print(f"items: {response.json()['items']}")
    # pprint(response.json().keys())
    # print("\n\n")
    return response


class XdcAndXrc20TransactionsByWallet:

    transactions_list = []
    page_number = 1

    def __init__(self, wallet_address, wallet_base_dir):
        self.wallet_address = wallet_address
        self.wallet_base_dir = wallet_base_dir

    def _transaction_parser(self, transactions: list) -> None:
        """
        Loop over the transactions. If symbol unknown then check its value. If the value is equal to 0 then pass, else
        make the symbol XDC and add item to transaction_list.
        If the symbol is known then add item to transaction list. 
        
        :param transactions: 
        """
        for item in transactions:
            if "symbol" not in item.keys():
                if item['value'] == 0:
                    pass
                else:
                    item["symbol"] = "XDC"
                    self.transactions_list.append(item)
            else:
                self.transactions_list.append(item)

    def _get_block_scan_transactions_from_server(self, coin_is_xrc20: bool) -> int:
        """
        First loop collects the transactions and passes them to the transaction_parser. If the coin_is_xrc20 parameter
        is False then it will collect xdc coin transactions. If its true then it will collect xrc-20 transactions.

        When the current page variable is equal to the total_pages variable the loop will stop

        :param coin_is_xrc20:
        :return:
        """
        get_more_pages = True
        total_pages = None
        current_page = 1

        base_url_of_block_scan = "https://xdc.blocksscan.io/api"

        xdc_url = f"{base_url_of_block_scan}/txs/listByAccount/{self.wallet_address}?tx_type=all"

        xrc20_url = f"{base_url_of_block_scan}/token-txs/xrc20?holder={self.wallet_address}"

        while get_more_pages:
            if current_page == 1:
                if coin_is_xrc20:
                    response = blockscan_response(url=xrc20_url).json()
                    transactions = response["items"]
                    total_pages = response["pages"]
                    self._transaction_parser(transactions=transactions)

                elif not coin_is_xrc20:
                    response = blockscan_response(url=xdc_url).json()
                    transactions = response["items"]
                    total_pages = response["pages"]
                    self._transaction_parser(transactions=transactions)

                if total_pages == current_page:
                    get_more_pages = False
                else:
                    current_page += 1

            else:
                if coin_is_xrc20:
                    xrc20_pagination_url = f"{xrc20_url}&page={current_page}"
                    response = blockscan_response(url=xrc20_pagination_url).json()
                    transactions = response["items"]
                    self._transaction_parser(transactions=transactions)

                elif not coin_is_xrc20:
                    xrc_pagination_url = f"{xdc_url}?page={current_page}"
                    response = blockscan_response(url=xrc_pagination_url).json()
                    transactions = response["items"]
                    self._transaction_parser(transactions=transactions)

                if total_pages == current_page:
                    get_more_pages = False
                else:
                    current_page += 1

        return total_pages

    def main(self):
        # Collect none xrc-20 transaction
        self._get_block_scan_transactions_from_server(coin_is_xrc20=False)

        # Collect xrc-20 transactions
        self._get_block_scan_transactions_from_server(coin_is_xrc20=True)

        return self.transactions_list


if __name__ == "__main__":
    wallet_info = ["brad_decent_wallet", "xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9"]
    wallet_name = wallet_info[0]
    wallet_address = wallet_info[1]
    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                   wallet_base_dir=wallet_name).main()

