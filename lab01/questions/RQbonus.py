import pandas as pd

csv = pd.read_csv("../repos.csv")

grupos_por_linguagem = csv.groupby('PrimaryLanguage')

rq2 = grupos_por_linguagem['Accepted Pull Requests'].apply(lambda x: x.median())
rq3 = grupos_por_linguagem['Total Releases'].apply(lambda x: x.median())
rq4 = grupos_por_linguagem['Time since last update'].apply(lambda x: x.median())
