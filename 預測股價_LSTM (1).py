import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from plotly.graph_objs import Scatter, Layout
from plotly.offline import plot
plt.rcParams["font.sans-serif"] = "mingliu"  #繪圖中文字型
plt.rcParams["axes.unicode_minus"] = False 

def load_data(df, dfp, sequence_length=10, split=0.8):
    #處理特徵資料
    data_all = np.array(df).astype(float)        # 轉為浮點型別矩陣
    # print(data_all.shape) # (242,3)
    data_all = scaler.fit_transform(data_all)    # 將特徵數據縮放為 0~1 之間
    #處理標籤資料
    datap_all = np.array(dfp).astype(float)      # 轉為浮點型別矩陣
    # print(datap_all.shape) # (242,1)
    datap_all = scalert.fit_transform(datap_all) # 將標籤數據縮放為 0~1 之間
    
    data = []  # ['收盤價','最高價','最低價']
    datap = [] # 收盤價
    # data、datap 資料共有 (242-10)=232 筆
    for i in range(len(data_all) - sequence_length):
        # 第 1~10天 的 ['收盤價','最高價','最低價'] 當作特徵
        data.append(data_all[i: i + sequence_length])
        # 第 11 天的收盤價當作標籤        
        datap.append(datap_all[i + sequence_length])
        
    x = np.array(data).astype('float64')  # 轉為浮點型別矩陣
    y = np.array(datap).astype('float64') # 轉為浮點型別矩陣 

    split_boundary = int(x.shape[0] * split)
    train_x = x[: split_boundary] # 前 80% 為 train 的特徵
    test_x = x[split_boundary:]   # 最後 20% 為 test 的特徵
 
    train_y = y[: split_boundary] # 前 80% 為 train 的 label
    test_y = y[split_boundary:]   # 最後 20% 為 test 的 label

    return train_x, train_y, test_x, test_y

def build_model():
    model = Sequential()     
    # 隱藏層：256 個神經元，input_shape：(10,3)
    # TIME_STEPS=10,INPUT_SIZE=3
    model.add(LSTM(input_shape=(10,3),units=256,unroll=False))
    model.add(Dense(units=1)) # 輸出層：1 個神經元
    #compile:loss, optimizer, metrics
    model.compile(loss="mse", optimizer="adam", metrics=['accuracy'])
    return model

def train_model(train_x, train_y, test_x, test_y):
    #訓練、預測並傳預測結果
    try:
        model.fit(train_x, train_y, batch_size=100, epochs=300, validation_split=0.1)
        predict = model.predict(test_x)
        predict = np.reshape(predict, (predict.size, )) #轉換為1維矩陣
    except KeyboardInterrupt:
        print(predict)
        print(test_y)
    return predict #傳回 預測值

# 主程式
pd.options.mode.chained_assignment = None  #取消顯示pandas資料重設警告
filename = 'twstockyear2019.csv'
df = pd.read_csv(filename, encoding='big5')#以pandas讀取檔案
ddtrain=df[['收盤價','最高價','最低價']]
ddprice=df[['收盤價']]

scaler = MinMaxScaler()  # 建立處理特徵的 MinMaxScaler 物件  
scalert = MinMaxScaler() # 建立處理標籤的 MinMaxScaler 物件    
train_x, train_y, test_x, test_y=load_data(ddtrain, ddprice, sequence_length=10, split=0.8)
# train_x 共 232*0.8=185 筆, test_x 共 232*0.2=47 筆
# print(train_x.shape,train_y.shape) # (185,10,3) (185,1)
# print(test_x.shape,test_y.shape)   # (47,10,3)  (47,1)

model = build_model() # 建立 RNN 模型
predict_y = train_model(train_x, train_y, test_x, test_y) # 訓練和預測
predict_y = scalert.inverse_transform([[i] for i in predict_y])   # 還原
test_y = scalert.inverse_transform(test_y)  # 還原

plt.plot(predict_y, 'b:') #預測
plt.plot(test_y, 'r-')    #收盤價
plt.legend(['預測', '收盤價'])
plt.show()

# 建立 DataFrame，加入 predict_y、test_y，準備以 plotly 繪圖
dd2=pd.DataFrame({"predict":list(predict_y),"label":list(test_y)})
#轉換為 numpy 陣列，並轉為 float
dd2["predict"] = np.array(dd2["predict"]).astype('float64')
dd2["label"] = np.array(dd2["label"]).astype('float64')

data = [
    Scatter(y=dd2["predict"],name='預測',line=dict(color="blue",dash="dot")),
    Scatter(y=dd2["label"],name='收盤價',line=dict(color="red"))
] 

plot({"data": data, "layout": Layout(title='2019年個股預測圖')},auto_open=True)