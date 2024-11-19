import json
import csv
from Currencies import Currencies


class DecoratorCurrencies(Currencies):
    def __init__(self, currencies=None):
        # super().__init__()
        self._currencies = currencies
    
    @property
    def currencies(self):
        return self._currencies
    
    def get_currencies(self):
        return self._currencies.get_currencies()
    
    def __str__(self):
        return super().__str__()

class CurrenciesJSON(DecoratorCurrencies):
    _currencies_json =None
    def get_currencies(self):
        res= super().get_currencies()
        if res:
            res_json= json.dumps(res, ensure_ascii=False)
            self._currencies_json = res_json
            return res_json
    
    def __str__(self):
        return self._currencies_json



class CurrenciesCSV(DecoratorCurrencies):
    _csv_filename="csv\\mycsvfile.csv"
    def get_currencies(self):
        res= super().get_currencies()
        res.pop('ValCurs')
        rows=[["ID", "CharCOde", "Name", "Value", "Nominal"]]
        if res:
            for ids in res :
                for key in res[ids]:
                    rows.append([ids, key, res[ids][key][0], res[ids][key][1], res[ids][key][2]])

            with open("csv\\mycsvfile.csv", "w", newline="", encoding='UTF-8') as f:
                w = csv.writer(f)
                w.writerows(rows)
            self._csv_filename="csv\\mycsvfile.csv"


    def __str__(self):
        import pandas as pd
        res = pd.read_csv(self._csv_filename)
        return str(res)

if __name__ == "__main__":
    a = Currencies()
    b = CurrenciesJSON(a).get_currencies()
    c = CurrenciesCSV(a).get_currencies()
    v = CurrenciesJSON(c).get_currencies()
    print(CurrenciesCSV(a))
    print(CurrenciesJSON(c))