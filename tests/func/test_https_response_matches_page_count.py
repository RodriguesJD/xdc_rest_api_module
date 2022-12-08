from blockscan_rest_api_module import XdcAndXrc20TransactionsByWallet
from pathlib import Path
import datetime

# TODO run code
# TODO capture folder path
# TODO Capture http responses/requests
# TODO Confirm number of responses to number of repsonse json files.

wallet_info = ["brad_decent_wallet", "xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9"]
wallet_name = wallet_info[0]
wallet_address = wallet_info[1]


class TestHttpsResponseMatchesJsonPages:

    path_to_dump_json = Path(f"{Path.cwd()}/temp_path/each_run/"
                             f"{datetime.datetime.now().strftime('%d-%m-%Y_time_%X_milsec_%f')}"
                             f"/blockscan_http_get_responses/")

    xdc_tx_class = XdcAndXrc20TransactionsByWallet(wallet_address=wallet_address,
                                                   directory_path=path_to_dump_json)
    test_url = 'https://xdc.blocksscan.io/api/txs/listByAccount/xdc33aab4f3e5500c27bb643cf9e503ba0d8939a8c9?tx_type=all'

    def test_http_and_pages_created(self):
        """
        Each https request should respond with transaction data.

        For the sake of trouble shooting in the future,confirming pre parsed data is nessacary.

        Each https response should be recorded in a json file. So the number of https responses and the number of json
        files in the blockscan_http_get_responses dir should be equal.
        """
        run_code = self.xdc_tx_class.main()
        txs_list = run_code[0]
        number_of_http_requests = run_code[1]

        assert isinstance(txs_list, list)
        assert isinstance(number_of_http_requests, int)

        json_count = 0
        for path in Path(self.path_to_dump_json).iterdir():
            if path.is_file():
                json_count += 1

        assert number_of_http_requests == json_count


