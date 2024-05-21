import pandas as pd
import csv,os,time,twstock

#pip install plotly 
from plotly.graph_objs import Scatter,Layout
from plotly.offline import plot

import matplotlib.pyplot as plt
import matplotlib


filepath = 'twstockyear2019_test1.csv'

if not os.path.isfile(filepath):  #如果檔案不存在就建立檔案
    title=["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
    outputfile = open(filepath, 'a', newline='', encoding='big5')  #開啟儲存檔案
    outputwriter = csv.writer(outputfile)  #以csv格式寫入檔案
    for i in range(1,7):  #設定下載的月份
        stock = twstock.Stock('2317')  # 建立 Stock 物件
        stocklist=stock.fetch(2019,i)  # stocklist 是存放第 "i" 月的 "所有交易日" 的 "所有" 股價資料
      
        data=[]  ## data 是存放第 "i" 月的 "所有交易日" 的 "自選項目" 股價資料. 輪到不同月份時就會清空.
        for stock in stocklist:  ## 迴圈變數 "stock" 與 stock = twstock.Stock('2317') 的 Stock 物件 同名, 較不好
            strdate=stock.date.strftime("%Y-%m-%d") #  將datetime物件轉換為字串
            # 讀取 日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數
            li=[strdate,stock.capacity,stock.turnover,stock.open,stock.high,stock.low,\
                stock.close,stock.change,stock.transaction]
            data.append(li) 

        if i==1:  #若是1月就寫入欄位名稱
            outputwriter.writerow(title) #寫入標題
        for dataline in (data):  #逐月寫入資料
            outputwriter.writerow(dataline)
        time.sleep(1)  #延遲1秒,否則有時會有錯誤
    outputfile.close()  #關閉檔案

pdstock = pd.read_csv(filepath, encoding='big5')  #以pandas讀取檔案
data = [
    Scatter(x=pdstock['日期'], y=pdstock['收盤價'], name='收盤價'),
    Scatter(x=pdstock['日期'], y=pdstock['最低價'], name='最低價'),
    Scatter(x=pdstock['日期'], y=pdstock['最高價'], name='最高價')
]


#### 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題



plot({"data": data, "layout": Layout(title='2019年個股統計圖')},auto_open=True)
