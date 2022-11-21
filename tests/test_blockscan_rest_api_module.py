from blockscan_rest_api_module import XdcAndXrc20TransactionsByWallet

wallet_info = ["brad_decent_wallet", "xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9"]
wallet_name = wallet_info[0]
wallet_address = wallet_info[1]


def test_wallet_transaction():
    all_wallet_transactions = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                              wallet_base_dir=wallet_name).main()
    assert isinstance(all_wallet_transactions, list)

    for transaction in all_wallet_transactions:
        assert isinstance(transaction, dict)
        # todo confirm the dict keys in the transactions.


class TestXdcAndXrc20TransactionsByWallet:

    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                   wallet_base_dir=wallet_name)

    def test_get_block_scan_data_from_server(self):
        url = 'https://xdc.blocksscan.io/api/txs/listByAccount/xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9?tx_type=all'
        total_pages = self.xdc_tx_class.get_block_scan_data_from_server(url=url)
        assert isinstance(total_pages, int)

