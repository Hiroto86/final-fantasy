import pandas as pd
import csv,os,time,twstock

#pip install plotly 
from plotly.graph_objs import Scatter,Layout
from plotly.offline import plot

filepath = 'twstockyear2019.csv'

if not os.path.isfile(filepath):  #如果檔案不存在就建立檔案
    title=["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
    outputfile = open(filepath, 'a', newline='', encoding='big5')  #開啟儲存檔案
    outputwriter = csv.writer(outputfile)  #以csv格式寫入檔案
    for i in range(1,7):  #設定下載的月份
        stock = twstock.Stock('2317')  # 建立 Stock 物件
        stocklist=stock.fetch(2019,i)
      
        data=[]
        for stock in stocklist:
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
plot({"data": data, "layout": Layout(title='2019年個股統計圖')},auto_open=True)