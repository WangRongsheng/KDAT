
# 代码描述：数据清洗第五步--- 数据分析，查看xml文件统计信息，生成数据报告

import pandas_profiling
import pandas as pd

def eda(in_file, out_file):
    data = pd.read_csv(in_file, sep=',')
    pfr = pandas_profiling.ProfileReport(data)
    pfr.to_file(out_file)


if __name__ == '__main__':
    in_file = 'dataset_Vehicle.csv'
    out_file = 'dataset_Vehicle.html'
    eda(in_file, out_file)
    print('eda done!')

