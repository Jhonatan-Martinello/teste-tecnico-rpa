import pandas as pd


class CsvReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_products(self):
        dataframe = pd.read_csv(self.file_path)

        return dataframe.to_dict("records")