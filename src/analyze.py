import json
import os
import pandas as pd

from glob import glob

from src.receipt import Receipt, BerkeleyBowlReceipt

receipt_class_dict = {
    'berkeley_bowl': BerkeleyBowlReceipt,
    'safeway': Receipt,
    'costco': Receipt,
    'trader_joes': Receipt,
    'target': Receipt,
    'ikea': Receipt,
    'other': Receipt,
}


def validate_items(
    output_dir: str,
    overwrite: bool=False,
):
    store_name, filename = output_dir.split('/')
    
    with open(f'outputs/{output_dir}/metadata.json', 'r') as file:
        json_data = json.load(file)
        # print(json_data)
        receipt = receipt_class_dict[store_name](**json_data)
        calculated_total = 0
        
        items = receipt.items
        for item in items:
            calculated_total += item['item_total_price']

        tax = receipt.tax if receipt.tax else 0
        total = receipt.total if receipt.total else 0

        # if calculated total+tax is within the same cents, then the itemization is valid
        if abs(calculated_total + tax - total) < 10 ** -2:
            print(f'Receipt items validated succesfully for {filename}!')

            if overwrite or not os.path.isfile(f'outputs/{output_dir}/items.csv'):
                items_df = pd.DataFrame(items)
                items_df.to_csv(f'outputs/{output_dir}/items.csv', index=False)


        else:
            print(f'There was an error in text validation for {filename}.')
            print(f'Calculated Total: {round(calculated_total, 2)}')
            print(f'Tax: {receipt.tax}')
            print(f'Calculated Total + Tax: {round(calculated_total + receipt.tax, 2)}')
            print(f'Total: {receipt.total}')


        

if __name__ == "__main__":
    skip = [
        # '20231222_berkeley_bowl',
        # '20231217_berkeley_bowl',
    ]

    stores = [store.split('/')[-1] for store in glob('outputs/*')]

    for store in stores:
        for file_path in glob(f'outputs/{store}/*'):
            if not (
                os.path.isfile(f'{file_path}/items.csv') or 
                any(filename in file_path for filename in skip)
            ):
            # if any(filename in file_path for filename in skip):
                print(file_path)
                output_dir = file_path.split('/', 1)[-1]
                validate_items(output_dir)