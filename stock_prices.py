'''
Написать функцию, которая возвращает максимальную прибыль от одной сделки
с одной акцией (сначала покупка, потом продажа). Исходные данные — массив
вчерашних котировок stock_prices_yesterday с ценами акций.

Информация о массиве:
Индекс равен количеству минут с начала торговой сессии (9:30 утра).
Значение в массиве равно стоимости акции в это время.

Например:
если акция в 10:00 утра стоила 20 долларов, то
stock_prices_yesterday[30] = 20.

Допустим, имеем некоторые условия:
stock_prices_yesterday = [10, 7, 5, 8, 11, 9]

profit = get_max_profit(stock_prices_yesterday)
#вернет 6 (купили за 5, продали за 11)

Массив может быть любым, хоть за весь день. Нужно написать функцию
get_max_profit как можно эффективнее — с наименьшими затратами времени
выполнения и памяти.
'''

import random
from _datetime import datetime, timedelta
import pandas as pd

'''
Для обработки выбран пандас по следущим причинам:
данные представлены как минимум с двемя параметрами
Использование вложенных (псевдомногомерных) массивов усложняет логику
Таким образом целесообразно работать с данными в табличном виде с возможностью масштабирования
Рвботу с такими данными предоставлется SQL, Pandas и Spark
Spark исключем как избыточный инструемент 
Pandas выигрывает в скорости обработки перед SQL
однако, на представленных объемах разница в скорости ничтожна, таким образом V(sql) ~ V(pandas)
Учитывая, что для получения исходного массива использовалась генерация данных на Python, в качестве инструмента обработки данных, в формате "единое окно" выбран Pandas 
'''
def init_rand_item(start: int, stop: int):
    return random.randint(start, stop + 1)


def init_time_point(time_point: str):
    return datetime.strptime(f'{time_point}:00', '%H:%M:00')


def init_data_frame(capacity: int):
    delta_sec = 0
    time_start_point = init_time_point('9:30')
    data = []

    # fill arr
    for index in range(capacity):
        arr = [index, init_rand_item(1, 20), (time_start_point + timedelta(0, delta_sec)).time()]
        data.append(arr)
        delta_sec += 60

    return pd.DataFrame(data, columns=['index', 'price', 'time'])


# return row from df based on condition 'index'
def stock_index_prices(index: int, df: pd.DataFrame):
    return df.loc[(df['index'] == index)][['index', 'price', 'time']]


def get_profit(df: pd.DataFrame):
    # get max value in col 'price'
    max_price = pd.Series(df['price']).max()

    # optionality, get row from df with max 'price' value
    df_max_price = df.loc[(df['price'] == max_price)][['index', 'price', 'time']]

    # find max index, that needs in a cases then we have a few max values in a different time points
    max_index_in_df_max_price = df_max_price['index'].max()

    # join row with index <= max in new data frame, and find there a min value of 'prise' col
    df_profit = df.iloc[:max_index_in_df_max_price + 1]
    min_price = pd.Series(df_profit['price']).min()

    # calculate diff between max - min and put the values and the result in a final data frame
    profit = max_price - min_price
    data = [[max_price, min_price, profit]]

    return pd.DataFrame(data, columns=['max_price', 'min price', 'profit'])


def run_app(df: pd.DataFrame):
    print(f'random data frame:\n{df}')
    print(f'price on time_point:\n{stock_index_prices(5, df)}')
    print(f'profit:\n{get_profit(df)}')


if __name__ == '__main__':
    run_app(init_data_frame(10))
