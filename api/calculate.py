import pandas as pd
import json

from glob import glob

def calculate(file_path, who_paid: str):
    df = pd.read_csv(file_path)

    output_dir = file_path.rsplit('/', 1)[0]
    date, store = output_dir.rsplit('/', 1)[-1].split('_', 1)
    print(f'{date[:4]}-{date[4:6]}-{date[6:]} @ {store}')

    receipt_dict = {}
    with open(f'{output_dir}/metadata.json', 'r') as file:
        json_data = json.load(file)

        receipt_dict['tax'] = json_data['tax'] if 'tax' in json_data else 0
        receipt_dict['total'] = json_data['total']

    b_tot, j_tot, t_tot = 0, 0, 0
    for i, row in df.iterrows():
        if row['paid_by'] == 'b':
            b_tot += row['item_total_price']
        elif row['paid_by'] == 'j':
            j_tot += row['item_total_price']
        elif row['paid_by'] == 't':
            t_tot += row['item_total_price']
    
    
    try:
        assert round(b_tot + j_tot + t_tot + receipt_dict['tax'], 2) == round(receipt_dict['total'], 2)
    except Exception as e:
        print(f'b_tot: {round(b_tot, 2)}')
        print(f'j_tot: {round(j_tot, 2)}')
        print(f't_tot: {round(t_tot, 2)}')
        print(f"tax: {receipt_dict['tax']}")
        print(f"total: {receipt_dict['total']}")
    else:
        b_portion = round(float(b_tot) + t_tot/2, 2)
        j_portion = round(float(j_tot) + t_tot/2, 2)

        try:
            assert abs(round(b_portion + j_portion + receipt_dict['tax'], 2) - round(receipt_dict['total'], 2)) < 1
        except Exception as e:
            print(f'Brendan Portion: {b_portion}')
            print(f'Jess Portion: {j_portion}')
            print(f"tax: {receipt_dict['tax']}")
            print(f"total: {receipt_dict['total']}")
        else:
            if who_paid == 'b':
                print(f'Jess pays Brendan {j_portion}')
            elif who_paid == 'j':
                print(f'Brendan pays Jess {b_portion}')
            else:
                print('ERRORRRRRR')

    print()

if __name__ == "__main__":
    # filepaths = [filepath.split('/')[-1].split('.')[0] for filepath in glob('assets/unverified/*')]
    
    # temp = [glob(f'outputs/*/{filepath}/items.csv')[0] for filepath in filepaths]
    # print(temp)

    paid_dict = {
        'outputs/berkeley_bowl/20240210_berkeley_bowl/items.csv': 'j', 
        'outputs/trader_joes/20240210_trader_joes/items.csv': 'b', 
        'outputs/target/20240219_target/items.csv': 'b', 
        'outputs/berkeley_bowl/20240220_berkeley_bowl/items.csv': 'b', 
        'outputs/trader_joes/20240221_trader_joes/items.csv': 'b',
    }


    for file_path in paid_dict.keys():
        calculate(file_path, paid_dict[file_path])
        