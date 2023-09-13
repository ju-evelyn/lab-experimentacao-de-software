import pandas as pd

csv = pd.read_csv("../repos.csv")

grupos_por_linguagem = csv.groupby('PrimaryLanguage')

rq2 = grupos_por_linguagem['Accepted Pull Requests'].apply(lambda x: x.median())
rq3 = grupos_por_linguagem['Total Releases'].apply(lambda x: x.median())
rq4 = grupos_por_linguagem['Time since last update'].apply(lambda x: x.median())


subset_most_popular_language = csv.loc[csv["Primary Language Number"] == 3]
subset_other_languages = csv.loc[csv["Primary Language Number"] != 3]

rq7_1 = subset_most_popular_language['Accepted Pull Requests'].median()
rq7_2 = subset_most_popular_language['Total Releases'].median()
rq7_3 = subset_most_popular_language['Time since last update'].median()

rq7_4 = subset_other_languages['Accepted Pull Requests'].median()
rq7_5 = subset_other_languages['Total Releases'].median()
rq7_6 = subset_other_languages['Time since last update'].median()
