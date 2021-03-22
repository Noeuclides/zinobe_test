import sys
import time
from fetch import FetchThreadCountry, FetchAsyncCountry, FetchCountry


if __name__ == '__main__':
    user_args = sys.argv
    if len(user_args) > 2:
        raise TypeError('Too many arguments. Check the README file.')
    t_i = time.perf_counter()
    if len(user_args) == 1:
        instance = FetchCountry()
    elif user_args[1] in ['async', 'a']:
        instance = FetchAsyncCountry()
    elif user_args[1] in ['thread', 't']:
        instance = FetchThreadCountry()
    else:
        raise TypeError('Not a valid option. Check the README file.')
    t_e = time.perf_counter()
    print(f'Execution time: {t_e - t_i:.6f}')
    # print(instance.regions_table)
    df = instance.create_df()
    print(df)
    instance.get_stats(df)
    instance.df_to_sql(df, 'country')
    instance.df_to_json(df, 'country')
