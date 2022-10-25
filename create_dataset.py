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
                proc = data_procedure.loc[(data_procedure['IADS-ID'].astype('float32') == float(row['IADS-ID']))
                                          & (data_procedure['IAPS-ID'].astype('float32') == float(row['IAPS-ID']))]

                if proc.empty:
                    continue
                if proc['COND'].values[0] == 'train':
                    continue
                if proc.size > 1:
                    proc = proc.iloc[0]

                data_combined.loc[index, 'ANS_VALENCE'] = proc['ANS-VALENCE']
                data_combined.loc[index, 'ANS_AROUSAL'] = proc['ANS-AROUSAL']
                data_combined.loc[index, 'ANS_TIME'] = proc['ANS-TIME']
                data_combined.loc[index, 'COND'] = proc['COND'][-1]
                last_iads = float(proc['IADS-ID'])
                last_iaps = float(proc['IAPS-ID'])
                last_valence = proc['ANS-VALENCE']
                last_arousal = proc['ANS-AROUSAL']
                last_time = proc['ANS-TIME']
                last_cond = proc['COND'][-1]

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
    data_final = data_final[data_final['ANS_AROUSAL'] > 0]
    data_final = data_final[data_final['ANS_VALENCE'] > 0]
    data_final.drop(columns='ANS_TIME', inplace=True)

    print('Writing data to file dataset.csv')
    data_final.to_csv('dataset.csv', index=False)

except FileNotFoundError:
    print('\n    ------------------------ ERROR ------------------------')
    print('''    This script requires two folders in the same directory:
    BIRAFFE2-photo - containing face csv files
    BIRAFFE2-procedure - containing procedure csv files''')
