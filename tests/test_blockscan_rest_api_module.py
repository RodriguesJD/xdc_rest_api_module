import requests
from pathlib import Path
import shutil
import datetime
import json
from blockscan_rest_api_module import XdcAndXrc20TransactionsByWallet, DumpXdcDataToJsonFile

wallet_info = ["brad_decent_wallet", "xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9"]
wallet_name = wallet_info[0]
wallet_address = wallet_info[1]


class TestXdcAndXrc20TransactionsByWallet:

    path_to_dump_json = Path(f"{Path.cwd()}/temp_path/each_run/"
                             f"{datetime.datetime.now().strftime('%d-%m-%Y_time_%X_milsec_%f')}"
                             f"/blockscan_http_get_responses/")

    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address, directory_path=path_to_dump_json)
    test_url = 'https://xdc.blocksscan.io/api/txs/listByAccount/xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9?tx_type=all'

    def test_blockscan_response(self):
        response = self.xdc_tx_class._blockscan_response_and_json_dump(url=self.test_url)
        assert response.json()
        assert str(response) == "<Response [200]>"
        # <class 'requests.models.Response'>
        assert str(response.status_code) == "200"

    def test_transaction_parser(self):
        """
        Gather transactions. Then pass it to the transaction_parser function. Check that the transaction list is empty
        before calling the function. Then test that the list is populated. Then clear the list and confirm its cleared.
        Clearing the list at the end cleans up the env for testing functions below.

        """
        response = requests.get(url=f"{self.test_url}").json()

        test_transactions = response["items"]
        tx_list = self.xdc_tx_class.transactions_list
        assert len(tx_list) == 0
        self.xdc_tx_class._transaction_parser(transactions=test_transactions)
        assert len(tx_list) > 0
        tx_list.clear()
        assert len(tx_list) == 0

    def test_get_block_scan_transactions_from_server(self):
        """
        get_block_scan_transactions_from_server calls to the api endpoint. Then it stores the xdc transaction
        data and returns the total number of pages needed to get all the wallet's transaction data.

        Note: I test that the transaction_list var from the class is empty. That way i know that
        get_block_scan_transactions_from_server hasn't added anything to that var yet.

        Then I call get_block_scan_data_from_server which should have now added dicts to the transaction_list var.

        I then test that the transaction list is now populated.

        Then I clear it, so it won't screw up testing functions below this one.

        """
        tx_list = self.xdc_tx_class.transactions_list
        assert len(tx_list) == 0
        total_pages = self.xdc_tx_class._get_block_scan_transactions_from_server(coin_is_xrc20=False)
        assert isinstance(total_pages, int)
        assert len(tx_list) > 0
        tx_list.clear()
        assert len(tx_list) == 0

    def test_main(self):
        all_wallet_transactions = self.xdc_tx_class.main()
        assert isinstance(all_wallet_transactions, list)

        for transaction in all_wallet_transactions:
            assert isinstance(transaction, dict)
            # todo confirm the dict keys in the transactions.
            key_list = ['_id', 'type', 'baseGasPrice', 'status', 'i_tx', 'blockHash', 'blockNumber', 'from', 'gas',
                        'gasPrice', 'hash', 'input', 'nonce', 'to', 'transactionIndex', 'value', 'createdAt',
                        'updatedAt', 'cumulativeGasUsed', 'from_model', 'gasUsed', 'timestamp', 'to_model', 'symbol',
                        'transactionHash', 'address', 'data', 'valueNumber', 'decimals', 'coingeckoID', 'fiatValue',
                        'blockTime']
            for key in list(transaction.keys()):
                assert key in key_list


class TestDumpXdcDataToJsonFile:

    file_name = "test_file.json"
    directory_path = Path(f"{Path.cwd()}/temp_path")
    complete_path = Path(f"{directory_path}/{file_name}") #  Mising json becuase the function adds

    data_to_dump = {"test": "testing"}

    dump_data_to_json = DumpXdcDataToJsonFile(filename=file_name,
                                              data_to_dump=data_to_dump,
                                              directory_path=directory_path)

    def test_path_does_not_exist(self):
        """
        If the testing path exist then remove it.
        """
        if self.directory_path.is_dir():
            shutil.rmtree(self.directory_path)
        assert not self.directory_path.is_dir()

    def test_dir_and_file_have_been_created(self):
        """
        Run class test that the dir and file was made.
        """
        self.dump_data_to_json.main()
        assert self.directory_path.is_dir()
        assert self.complete_path.is_file()

    def test_file_has_correct_data(self):
        """
        Confirm the correct data was written to the file.
        """
        with open(self.complete_path, "r") as read_file:
            data = json.load(read_file)
            assert data["test"] == "testing"
