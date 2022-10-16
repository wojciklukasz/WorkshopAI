import os
import pandas as pd

data_final = pd.DataFrame()

try:
    for file in os.listdir('BIRAFFE2-photo'):
        subject = file[:6]
        print(f'Processing data for {subject}')

        data_photo = pd.read_csv(f'BIRAFFE2-photo/{subject}-Face.csv', delimiter=';', dtype='str')
        data_procedure = pd.read_csv(f'BIRAFFE2-procedure/{subject}-Procedure.csv', delimiter=';', dtype='str')
        data_procedure = data_procedure[data_procedure['COND'].notna()]
        data_procedure.replace('None', '-1', inplace=True)

        data_combined = data_photo.iloc[:, 2:][data_photo['FRAME-NUMBER'].isin(['0', '105', '120', '135', '15', '150'])].fillna(-1)
        data_combined['ANS_VALENCE'] = '0'
        data_combined['ANS_AROUSAL'] = '0'
        data_combined['ANS_TIME'] = '0'
        data_combined['COND'] = '0'

        last_iads = -1
        last_iaps = -1
        last_valence = -1
        last_arousal = -1
        last_time = -1
        last_cond = -1

        for index, row in data_combined.iterrows():
            if float(row['IADS-ID']) == last_iads and float(row['IAPS-ID']) == last_iaps:
                data_combined.loc[index, 'ANS_VALENCE'] = last_valence
                data_combined.loc[index, 'ANS_AROUSAL'] = last_arousal
                data_combined.loc[index, 'ANS_TIME'] = last_time
                data_combined.loc[index, 'COND'] = last_cond
            else:
                for index2, row2 in data_procedure.iterrows():
                    if float(row['IADS-ID']) == float(row2['IADS-ID']) and float(row['IAPS-ID']) == float(row2['IAPS-ID']):
                        data_combined.loc[index, 'ANS_VALENCE'] = row2['ANS-VALENCE']
                        data_combined.loc[index, 'ANS_AROUSAL'] = row2['ANS-AROUSAL']
                        data_combined.loc[index, 'ANS_TIME'] = row2['ANS-TIME']
                        data_combined.loc[index, 'COND'] = row2['COND'][-1]
                        last_iads = float(row2['IADS-ID'])
                        last_iaps = float(row2['IAPS-ID'])
                        last_valence = row2['ANS-VALENCE']
                        last_arousal = row2['ANS-AROUSAL']
                        last_time = row2['ANS-TIME']
                        last_cond = row2['COND'][-1]
                        break

        data_combined = data_combined.iloc[:, 2:]

        if data_final.empty:
            data_final = data_combined
        else:
            data_final = pd.concat([data_final, data_combined])

    data_final = data_final.astype(
        {
            'ANGER': 'float64',
            'CONTEMPT': 'float64',
            'DISGUST': 'float64',
            'FEAR': 'float64',
            'HAPPINESS': 'float64',
            'NEUTRAL': 'float64',
            'SADNESS': 'float64',
            'SURPRISE': 'float64',
            'ANS_TIME': 'float64',
            'ANS_VALENCE': 'float64',
            'ANS_AROUSAL': 'float64',
            'COND': 'string'
        }
    )

    data_final = data_final[data_final['ANGER'] >= 0]
    data_final = data_final[data_final['CONTEMPT'] >= 0]
    data_final = data_final[data_final['DISGUST'] >= 0]
    data_final = data_final[data_final['FEAR'] >= 0]
    data_final = data_final[data_final['HAPPINESS'] >= 0]
    data_final = data_final[data_final['NEUTRAL'] >= 0]
    data_final = data_final[data_final['SADNESS'] >= 0]
    data_final = data_final[data_final['SURPRISE'] >= 0]
    data_final = data_final[data_final['ANS_TIME'] >= 0]
    data_final.drop(columns='ANS_TIME', inplace=True)
    data_final = data_final[data_final['COND'] != 'n']

    print('Writing data to file dataset.csv')
    data_final.to_csv('dataset.csv', index=False)

except FileNotFoundError:
    print('\n    ------------------------ ERROR ------------------------')
    print('''    This script requires two folders in the same directory:
    BIRAFFE2-photo - containing face csv files
    BIRAFFE2-procedure - containing procedure csv files''')
