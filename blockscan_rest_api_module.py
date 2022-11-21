import requests
from pprint import pprint
import json


class XdcAndXrc20TransactionsByWallet:

    transactions_list = []
    base_url_of_block_scan = "https://xdc.blocksscan.io/api"
    page_number = 1

    def __init__(self, wallet_address, wallet_base_dir):
        self.wallet_address = wallet_address
        self.wallet_base_dir = wallet_base_dir

        self.xdc_url = f"{self.base_url_of_block_scan}/txs/listByAccount/{self.wallet_address}?tx_type=all"
        self.xrc20_url = f"{self.base_url_of_block_scan}/token-txs/xrc20?holder={self.wallet_address}"

    def transaction_parser(self, transactions: list) -> None:
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

    def get_block_scan_data_from_server(self, url: str) -> int:
        """
        Request to the server using the parameter url. Collect the total page and the transaction data. Then add the
        transaction data to the transaction_parser function. Return the number of pages to be uses by the
        transaction_parser.

        :param url: This is built from the base_url_of_block_scan var.
        :return total_pages: The total number of pages that are needed to collect all the transaction data.
        """
        response = requests.get(url=f"{url}").json()
        transactions = response["items"]
        total_pages = response["pages"]

        self.transaction_parser(transactions=transactions)

        return total_pages

    def paginate_request(self, url):
        response = requests.get(url).json()
        return response

    def pagination_page_counter(self, base_url, total_pages):
        if total_pages > 1:
            while total_pages != 1:
                self.page_number += 1
                url = f"{base_url}?page={self.page_number}"
                if "token-txs/" in url:
                    pagination_response = self.paginate_request(url=f"{base_url}&page={self.page_number}")
                else:
                    pagination_response = self.paginate_request(url=f"{base_url}?page={self.page_number}")

                transactions = pagination_response["items"]
                self.transaction_parser(transactions=transactions)
                total_pages -= 1

        self.page_number = 1

    def post_collection_data(self):
        txs = self.transactions_list
        print(f"list_size:{len(txs)}")

        for transaction in txs:
            print(transaction['blockNumber'])

    def main(self):
        scan_xdc_and_return_total_pages = self.get_block_scan_data_from_server(url=self.xdc_url)
        xdc_total_pages = scan_xdc_and_return_total_pages
        self.pagination_page_counter(base_url=self.xdc_url, total_pages=xdc_total_pages)

        scan_xrc20s_and_return_page_number = self.get_block_scan_data_from_server(url=self.xrc20_url)
        xrc20_total_pages = scan_xrc20s_and_return_page_number
        self.pagination_page_counter(base_url=self.xrc20_url, total_pages=xrc20_total_pages)

        # self.post_collection_data()
        return self.transactions_list


