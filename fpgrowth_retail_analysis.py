"""
fpgrowth_retail_analysis.py

Опис: Цей скрипт використовує алгоритм FP-Growth для аналізу асоціативних правил у датасеті роздрібних продажів. 

Автор: Кацай Дар'я
Дата створення: 27 липня 2023 року
"""


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth


def filter_and_save_data(fname):
    """
    Фільтрує та зберігає оброблені дані з вхідного файлу Excel.
    
    :param fname: Шлях до файлу Excel з даними.
    :return: DataFrame з обробленими даними.
    """

    # read data with excel file
    online_retail = pd.read_excel(fname)
    
    # check the data in 'InvoiceNo'
    online_retail['Invoice'] = pd.to_numeric(online_retail['Invoice'], errors='coerce')
    
    # filter data
    online_retail = online_retail[online_retail['Price'] > 0]
    online_retail = online_retail[(online_retail['Quantity'] > 0) & (online_retail['Quantity'] >= 1000)].drop_duplicates().dropna()
    
    # data grouping in DataFrameGroupBy
    grouped_transactions = online_retail.groupby('Invoice')['Description'].apply(tuple)
    
    # convert data to a DataFrame with boolean values
    te = TransactionEncoder()
    te_ary = te.fit(grouped_transactions).transform(grouped_transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df


def get_recommendations(df):

    """
    Генерує рекомендації товарів на основі вхідних даних.
    
    :param df: DataFrame з обробленими даними.
    :return: DataFrame з топ-10 рекомендаціями.
    """

    
    # find frequent itemsets with minimum support
    patterns = fpgrowth(df, min_support=0.022, use_colnames=True)
    
    # filter patterns to keep only those with at least 3 itemsets
    patterns = patterns[patterns['itemsets'].apply(lambda x: len(x) == 3)]
    
    # sort patterns by support in descending order
    patterns = patterns.sort_values(by='support', ascending=False)
    patterns.to_excel('recommendation.xlsx')

    return patterns.head(10)
    
    
dataframe = filter_and_save_data('online_retail_2.xlsx')
results = get_recommendations(dataframe)
print(results)

