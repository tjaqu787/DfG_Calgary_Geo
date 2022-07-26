import pandas
from sodapy import Socrata
import os.path


def get_connector_data():

    source_hostname="data.calgary.ca"
    pathways_endpoint = "6eun-p5zf"
    file_name = "pathways.pkl"
    if not os.path.exists(file_name):
        print(f'{file_name} does not exist. Downloading new data...')
        client = Socrata('data.calgary.ca', None)
        results = client.get(pathways_endpoint)
        dataframe = pandas.DataFrame.from_records(results)
        print(f'Data downloaded. Saving to {file_name}...')
        dataframe.to_json(file_name)
    else:
        print(f'{file_name} exists. Loading data from disk...')
        dataframe = pandas.read_json(file_name)


    return dataframe


if __name__ == '__main__':
    get_connector_data()