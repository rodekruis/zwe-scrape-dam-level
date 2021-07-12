import datetime
import os
import requests
import pandas as pd
from pipeline.utils import get_blob_service_client
import logging
import re
import datetime
import click
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='ex.log')
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


@click.command()
@click.option('--nodatalake', is_flag=True, help='upload to Azure datalake')
def main(nodatalake):

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:
        source = requests.get('https://www.zinwa.co.zw/dam-levels/', 'html.parser').text
        date_str = re.search("Dam Levels as at (.*?)\<\/h", source).group(1)
        date_time_obj = datetime.datetime.strptime(date_str, '%d-%B-%Y')
        date = date_time_obj.date()

        tables = pd.read_html("https://www.zinwa.co.zw/dam-levels/")
        if len(tables) < 1:
            logging.error("PIPELINE ERROR: table not found")
        else:
            table = tables[0]
            # remove first line (NaNs)
            table = table.drop([0])
            # remove last column
            if "Unnamed: 4" in table.columns:
                table = table.drop(columns=["Unnamed: 4"])
            print(table)

            # save locally
            data_path = 'zwe_dam_levels.csv'
            table.to_csv(data_path)

            # upload to datalake
            if not nodatalake:
                # operational (latest data)
                blob_client = get_blob_service_client('drought/Silver/zwe/zwe_dam_levels.csv')
                with open(data_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)

                # archive (date-stamped data)
                blob_client = get_blob_service_client(f"drought/Silver/zwe/archive/zwe_dam_levels_{date.strftime('%d_%b_%Y')}.csv")
                with open(data_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
    except Exception as e:
        logging.error(f"PIPELINE ERROR: {e}")

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


if __name__ == "__main__":
    main()