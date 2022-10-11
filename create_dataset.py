import pandas as pd

data_photo = pd.read_csv('BIRAFFE2-photo/SUB103-Face.csv', delimiter=';')
data_procedure = pd.read_csv('BIRAFFE2-procedure/SUB103-Procedure.csv', delimiter=';')
data_procedure = data_procedure[data_procedure['COND'].notna()]
data_procedure.replace('None', -1, inplace=True)

data_combined = data_photo.iloc[:, 2:][data_photo['FRAME-NUMBER'].isin([0, 105, 120, 135, 15, 150])].fillna(-1)
data_combined['ANS_VALENCE'] = 0
data_combined['ANS_AROUSAL'] = 0

for index, row in data_combined.iterrows():
    for index2, row2 in data_procedure.iterrows():
        if float(row['IADS-ID']) == float(row2['IADS-ID']) and float(row['IAPS-ID']) == float(row2['IAPS-ID']):
            data_combined.loc[index, 'ANS_VALENCE'] = row2['ANS-VALENCE']
            data_combined.loc[index, 'ANS_AROUSAL'] = row2['ANS-AROUSAL']
            break

data_combined = data_combined.iloc[:, 2:]
print(data_combined)

data_combined.to_csv('dataset.csv', index=False)
