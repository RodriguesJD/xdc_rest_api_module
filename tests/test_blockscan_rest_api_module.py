import requests

from blockscan_rest_api_module import XdcAndXrc20TransactionsByWallet

wallet_info = ["brad_decent_wallet", "xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9"]
wallet_name = wallet_info[0]
wallet_address = wallet_info[1]


class TestXdcAndXrc20TransactionsByWallet:

    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                   wallet_base_dir=wallet_name)
    test_url = 'https://xdc.blocksscan.io/api/txs/listByAccount/xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9?tx_type=all'

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


def test_transaction_count_matches_json_count():
    """
    The number of json file created with the f"{time_stamp}_blockscan_response".json should be the same as the
    transaction counter
    :return:
    """
    pass


