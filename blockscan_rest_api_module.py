import requests
from pprint import pprint
import json
import datetime
import os
from pathlib import Path


class DumpXdcDataToJsonFile:

    def __init__(self, filename, data_to_dump, directory_path=Path.cwd()):
        self.filename = filename
        self.data_to_dump = data_to_dump
        self.directory_path = directory_path

    def main(self):
        """
        If path doesnt exist then create it.

        Write data to a json file using the defualt or provided directory path.

        """
        if Path.exists(self.directory_path):
            pass
        else:
            Path(self.directory_path).mkdir(parents=True, exist_ok=True)

        if ".json" in self.filename:
            self.filename = Path(f"{str(self.filename).replace('.json', '')}")  # if .json in file, remove it

        file_with_path = f"{self.directory_path}/{self.filename}.json"
        with open(file_with_path, "w") as write_file:
            json.dump(self.data_to_dump, write_file)


class XdcAndXrc20TransactionsByWallet:

    def __init__(self, wallet_address: str, directory_path=Path.cwd()):
        self.wallet_address = wallet_address
        self.directory_path = directory_path
        self.transactions_list = []
        self.page_number = 1
        self.http_request_counter = 0

    def _blockscan_response_and_json_dump(self, url: str) -> requests.models.Response:
        """
        Keeps track of each transaction by incrementing the http_request_counter by 1, each time a http requests is 
        made.
        
        Create the time stamp to be used for file_name creation
        
        Create the file name.
        
        Create dict to be used for writing json for each http request.
        
        Pass dict to the write_to_dump func

        :param url: 
        :return resonse: 
        """
        # TODO create type hinting, code comments,
        # TODO turn write to json off by defualt
        self.http_request_counter += 1
        response = requests.get(url=f"{url}")
        time_stamp = datetime.datetime.now().strftime("%d-%m-%Y_time_%X_milsec_%f")
        file_name = f"{time_stamp}_blockscan_response"
        data_to_dump = dict(response.json())
        data_to_dump["url"] = url
        data_to_dump["headers"] = json.dumps(dict(response.headers))
        DumpXdcDataToJsonFile(filename=file_name, data_to_dump=data_to_dump, directory_path=self.directory_path).main()
        return response

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
                    response = self._blockscan_response_and_json_dump(url=xrc20_url).json()
                    transactions = response["items"]
                    total_pages = response["pages"]
                    self._transaction_parser(transactions=transactions)

                elif not coin_is_xrc20:
                    response = self._blockscan_response_and_json_dump(url=xdc_url).json()
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
                    response = self._blockscan_response_and_json_dump(url=xrc20_pagination_url).json()
                    transactions = response["items"]
                    self._transaction_parser(transactions=transactions)

                elif not coin_is_xrc20:
                    xrc_pagination_url = f"{xdc_url}?page={current_page}"
                    response = self._blockscan_response_and_json_dump(url=xrc_pagination_url).json()
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
    path_to_dump_json = Path(f"{Path.cwd()}/each_run/{datetime.datetime.now().strftime('%d-%m-%Y_time_%X_milsec_%f')}"
                             f"/blockscan_http_get_responses/")
    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                   directory_path=path_to_dump_json).main()

