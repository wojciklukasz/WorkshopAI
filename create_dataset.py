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

        for index, row in data_combined.iterrows():
            for index2, row2 in data_procedure.iterrows():
                if float(row['IADS-ID']) == float(row2['IADS-ID']) and float(row['IAPS-ID']) == float(row2['IAPS-ID']):
                    data_combined.loc[index, 'ANS_VALENCE'] = row2['ANS-VALENCE']
                    data_combined.loc[index, 'ANS_AROUSAL'] = row2['ANS-AROUSAL']
                    data_combined.loc[index, 'ANS_TIME'] = row2['ANS-TIME']
                    break

        data_combined = data_combined.iloc[:, 2:]

        if data_final.empty:
            data_final = data_combined
        else:
            data_final = pd.concat([data_final, data_combined])

    data_final = data_final.astype('float64')
    data_final = data_final[data_final['ANGER'] >= 0]
    data_final = data_final[data_final['CONTEMPT'] >= 0]
    data_final = data_final[data_final['DISGUST'] >= 0]
    data_final = data_final[data_final['FEAR'] >= 0]
    data_final = data_final[data_final['HAPPINESS'] >= 0]
    data_final = data_final[data_final['NEUTRAL'] >= 0]
    data_final = data_final[data_final['SADNESS'] >= 0]
    data_final = data_final[data_final['SURPRISE'] >= 0]
    data_final = data_final[data_final['ANS_TIME'] >= 0]
    data_final = data_final.iloc[:, :-1]

    print('Writing data to file dataset.csv')
    data_final.to_csv('dataset.csv', index=False)

except FileNotFoundError:
    print('\n    ------------------------ ERROR ------------------------')
    print('''    This script requires two folders in the same directory:
    BIRAFFE2-photo - containing face csv files
    BIRAFFE2-procedure - containing procedure csv files''')
