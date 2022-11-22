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
        self.xdc_tx_class.transaction_parser(transactions=test_transactions)
        assert len(tx_list) > 0
        tx_list.clear()
        assert len(tx_list) == 0

    def test_get_block_scan_data_from_server(self):
        """
        get_block_scan_data_from_server makes the first call to the api endpoint. Then it stores the xdc transaction
        data and returns the total number of pages needed to get all the wallet's transaction data.

        Note: I test that the transaction_list var from the class is empty. That way i know that
        get_block_scan_data_from_server hasn't added anything to that var yet.

        Then I call get_block_scan_data_from_server which should have now added dicts to the transaction_list var.

        I then test that the transaction list is now populated.

        Then I clear it so it won't screw up testing functions below this one.

        """
        tx_list = self.xdc_tx_class.transactions_list
        assert len(tx_list) == 0
        total_pages = self.xdc_tx_class.get_block_scan_data_from_server(url=self.test_url)
        assert isinstance(total_pages, int)
        assert len(tx_list) > 0
        tx_list.clear()
        assert len(tx_list) == 0

    def test_paginate_request(self):
        """
        This is much like get_block_scan_data_from_server but it simply calls the url and returns the response.
        """
        assert isinstance(self.xdc_tx_class.paginate_request(url=self.test_url), dict)

    def test_main(self):
        all_wallet_transactions = self.xdc_tx_class.main()
        assert isinstance(all_wallet_transactions, list)

        for transaction in all_wallet_transactions:
            assert isinstance(transaction, dict)
            # todo confirm the dict keys in the transactions.

