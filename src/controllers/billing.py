from src.helpers import helpers
from src.helpers.helpers import return_date_time_combined
from src.utils import prompts
class Billing:
    def __init__(self):
        self.sql_queries = helpers.get_sql_queries()
        pass

    def calculate_charges(self, charges: int, hours_parked_for):
        if hours_parked_for > 0:
            total_charges = hours_parked_for * charges
            return total_charges
        return 1 * charges

    def _print_bill(self, bill):
        print(prompts.BILL_FORMAT.format(*bill))

    def generate_bill(self, billing_id):
        data = self.db.get_multiple_items(
            self.sql_queries["get_billing_details"], (billing_id,))
        if not data:
            print("Bill ID do not Exists.")
            return
        bill = data[0]
        bill = list(bill)
        _date = bill[7]
        _time = bill[8]
        date_time = return_date_time_combined(_date, _time)
        bill[8] = date_time
        bill.pop(7)
        self._print_bill(bill)