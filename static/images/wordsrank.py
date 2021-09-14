#-*-coding:utf-8-*-
import numpy as np
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MO, TU
from datetime import datetime
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import mysql.connector
from tqdm import tqdm
import time
from matplotlib.font_manager import _rebuild

_rebuild()


pymysql.install_as_MySQLdb()


ce = create_engine("mysql+mysqlconnector://root:******@localhost:3306/rhyme", encoding='utf-8')
sql1 = "select words,times from `Cihai` where times>=1 order by times desc limit 10"
data1 = pd.read_sql_query(sql1, con=ce)
print(data1)
data1 = data1.set_index(data1['times']).sort_index(ascending=True)
fig1 = plt.figure(figsize=(9, 16))
ax1 = fig1.add_subplot(1,1,1)
#data1['ratio'].plot(label='比值')
plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus'] = False
xs = [d for d in data1['words']]
#xmajorLocator = MultipleLocator(5)  # 定义横向主刻度标签的刻度差为2的倍数。就是隔几个刻度才显示一个标签文本
plt.barh(xs, data1.index, color=['c', 'g', 'b', 'y', 'm', 'r', 'grey', 'gold', 'darkviolet', 'turquoise'], label='热词TOP10')
plt.xticks([])# 不显示x轴
plt.yticks(size='medium', rotation=45, fontsize=16)
ax1.legend(loc='upper left')

ax1.set_title('更新时间：{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), fontsize=16)
plt.savefig('rank.png')
plt.show()

