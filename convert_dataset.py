import pandas as pd
from scipy.io import arff


data, meta = arff.loadarff('phishing+websites.arff')
df = pd.DataFrame(data)


df = df.applymap(lambda x: int(x.decode()) if isinstance(x, bytes) else x)


df['Result'] = df['Result'].map({-1: 1, 1: 0}) 
df.rename(columns={'Result': 'label'}, inplace=True)

df.to_csv('data/phishing_dataset.csv', index=False)
print(f"Dataset sauvegardé : {len(df)} lignes, {len(df.columns)} colonnes")
print(df['label'].value_counts())