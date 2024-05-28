# 載入必要套件
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

#import numpy as np
import time
#from haohaninfo import MicroPlay
#M = MicroPlay.MicroPlayCommand()
#a = MicroPlay.MicroPlayQuote() 
#GOC = haohaninfo.GOrder.GOCommand()
#GOQ = haohaninfo.GOrder.GOQuote()

# 下單部位管理物件
class Record():
    def __init__(self ):
        # 儲存績效
        self.Profit=[]
        # 未平倉
        self.OpenInterestQty=0
        self.OpenInterest=[]
        # 交易紀錄總計
        self.TradeRecord=[]
    # 進場紀錄
    def Order(self, BS,Product,OrderTime,OrderPrice,OrderQty):
        if BS=='B' or BS=='Buy':
            for i in range(int(OrderQty)):
                self.OpenInterest.append([1,Product,OrderTime,OrderPrice])  ## OpenInterest 中的每一個記錄都是一口
                self.OpenInterestQty +=1
        elif BS=='S' or BS=='Sell':
            for i in range(int(OrderQty)):
                self.OpenInterest.append([-1,Product,OrderTime,OrderPrice])  ## OpenInterest 中的每一個記錄都是一口
                self.OpenInterestQty -=1
    # 出場紀錄(買賣別需與進場相反，多單進場則空單出場)
    def Cover(self, BS,Product,CoverTime,CoverPrice,CoverQty):
        if BS=='S' or BS=='Sell':
            for i in range(int(CoverQty)):
                # 取得多單未平倉部位
                TmpInterest=[ j for j in self.OpenInterest if j[0]==1 ][0]
                if TmpInterest != []:
                    # 清除未平倉紀錄
                    self.OpenInterest.remove(TmpInterest)
                    self.OpenInterestQty -=1
                    # 新增交易紀錄(已經平倉), TradeRecord 中的每一個記錄都是一口
                    self.TradeRecord.append(['B',TmpInterest[1],TmpInterest[2],TmpInterest[3],CoverTime,CoverPrice])  ## 'B' 代表進場是多單 ##TmpInterest[1]:Product, TmpInterest[2]:OrderTime, TmpInterest[3]:OrderPrice 
                    self.Profit.append(CoverPrice-TmpInterest[3])
                else:
                    print('尚無進場')
        elif BS=='B' or BS=='Buy':
            for i in range(int(CoverQty)):
                # 取得空單未平倉部位
                TmpInterest=[ k for k in self.OpenInterest if k[0]==-1 ][0]
                if TmpInterest != []:
                    # 清除未平倉紀錄
                    self.OpenInterest.remove(TmpInterest)
                    self.OpenInterestQty +=1
                    # 新增交易紀錄
                    self.TradeRecord.append(['S',TmpInterest[1],TmpInterest[2],TmpInterest[3],CoverTime,CoverPrice])  ## 'S' 代表進場是空單
                    self.Profit.append(TmpInterest[3]-CoverPrice)
                else:
                    print('尚無進場')
    # 取得當前未平倉量
    def GetOpenInterest(self):               
        return self.OpenInterestQty
    # 取得交易紀錄
    def GetTradeRecord(self):               
        return self.TradeRecord   
    # 取得交易績效
    def GetProfit(self):       
        return self.Profit  
    # # 將股票的回測紀錄寫入MicroTest當中
    # def StockMicroTestRecord(self,StrategyName,Discount):
    #     microtest_db.login('jack','1234','ftserver.haohaninfo.com')
    #     for row in self.TradeRecord:
    #         Fee=row[3]*1000*0.001425*Discount + row[5]*1000*0.001425*Discount 
    #         Tax=row[5]*1000*0.003
    #         microtest_db.insert_to_server_db(   \
    #         row[1],                             \
    #         row[2].strftime('%Y-%m-%d'),        \
    #         row[2].strftime('%H:%M:%S'),        \
    #         row[3],                             \
    #         row[0],                             \
    #         '1',                                \
    #         row[4].strftime('%Y-%m-%d'),        \
    #         row[4].strftime('%H:%M:%S'),        \
    #         row[5],                             \
    #         Tax,                                \
    #         Fee,                                \
    #         StrategyName)    
    #     microtest_db.commit()
    # 將期貨的回測紀錄寫入MicroTest當中
#    def FutureMicroTestRecord(self,StrategyName,ProductValue,Fee):   ## StrategyName不能出現中文
#        #microtest_db.login('jack','1234','ftserver.haohaninfo.com')
#        microtest_db.login('pu25','pu25','140.128.36.207')
#        #microtest_db.login(account,password,'140.128.36.207')
#        for row in self.TradeRecord:
#            Tax=(row[3]+row[5])*ProductValue*0.00002  ##原來是錯誤的: Tax=row[5]*ProductValue*0.00002*2
#            microtest_db.insert_to_server_db(   \
#            row[1],                             \
#            row[2].strftime('%Y-%m-%d'),        \
#            row[2].strftime('%H:%M:%S'),        \
#            str(int(row[3])),                             \
#            str(row[0]),                             \
#            '1',                                \
#            row[4].strftime('%Y-%m-%d'),        \
#            row[4].strftime('%H:%M:%S'),        \
#            str(row[5]),                             \
#            str(int(Tax)),                                \
#            str(int(Fee)),                                \
#            StrategyName) 
#        microtest_db.commit()
        
        
    # def FutureMicroTestRecord(self,StrategyName,ProductValue,Fee,volume,account,password):
    #     #microtest_db.login('jack','1234','ftserver.haohaninfo.com')
    #     microtest_db.login(account,password,'140.128.36.207')
    #     #microtest_db.login(account,password,'140.128.36.207')
    #     for row in self.TradeRecord:
    #         Tax=(row[3]+row[5])*ProductValue*0.00002
    #         microtest_db.insert_to_server_db(row[1],row[2].strftime('%Y-%m-%d'),row[2].strftime('%H:%M:%S'),str(int(row[3])),str(row[0]),str(volume),row[4].strftime('%Y-%m-%d'),row[4].strftime('%H:%M:%S'),str(row[5]),str(int(Tax)),str(int(Fee)),StrategyName) 
    #     microtest_db.commit()
    
    # 取得交易績效
    def GetTotalProfit(self):  
        return sum(self.Profit)
    # 取得平均交易績效
    def GetAverageProfit(self): 
        return sum(self.Profit)/len(self.Profit)
        
    # 取得勝率
    def GetWinRate(self):
        WinProfit = [ i for i in self.Profit if i > 0 ]
        return len(WinProfit)/len(self.Profit)
    # 最大連續虧損
    def GetAccLoss(self):
        AccLoss = 0
        MaxAccLoss = 0
        for p in self.Profit:
            if p <= 0:
                AccLoss+=p
                if AccLoss < MaxAccLoss:
                    MaxAccLoss=AccLoss
            else:
                AccLoss=0  ##因為是要計算 "連續" 虧損,一旦中間有賺錢，就中斷連續虧損
        return MaxAccLoss
    # 最大資金(績效)回落(MDD)
    def GetMDD(self):
        MDD,Capital,MaxCapital = 0,0,0
        for p in self.Profit:
            Capital += p
            MaxCapital = max(MaxCapital,Capital)
            DD = MaxCapital - Capital
            MDD = max(MDD,DD)
        return MDD
    # 平均獲利 
    def GetAverEarn(self):
        WinProfit = [ i for i in self.Profit if i > 0 ]
        if len(WinProfit)>0:
           return sum(WinProfit)/len(WinProfit)
        if len(WinProfit)==0:
           return '沒有賺錢記錄'
    # 平均虧損
    def GetAverLoss(self):
        FailProfit = [ i for i in self.Profit if i < 0 ]
        if len(FailProfit)>0:
           return sum(FailProfit)/len(FailProfit)
        if len(FailProfit)==0:
           return '沒有賠錢記錄'
            
    # 產出交易績效圖
    def GeneratorProfitChart(self,StrategyName='Strategy'):
        # 定義圖表
        ax1 = plt.subplot(111)
        # 計算累計績效
        TotalProfit=[0]
        for i in self.Profit:
            TotalProfit.append(TotalProfit[-1]+i)
        # 繪製圖形
        ax1.plot( TotalProfit  , '-', linewidth=1 )
        #定義標頭
        ax1.set_title('Accumulated Profit(累計淨績效)')
        plt.show()    # 顯示繪製圖表
        # plt.savefig(StrategyName+'.png') #儲存繪製圖表
    

    

# # 市價委託單(預設非當沖、倉別自動)
# #def OrderMKT(Broker,Product,BS,Qty,DayTrade='0',OrderType='A'):
# def OrderMKT(Broker,Product,BS,Qty,DayTrade='0'):
#     # 送出交易委託
#     # print([Broker, Product, BS, '',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType])
#     #OrderNo=GOC.Order(Broker, Product, BS, '0',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType)  ##此為元富期貨的例子: OrderType為 "下單類別"： A（ 自動） 、 N（ 新倉） 、 C（ 平倉）， 預設值為 A
#     OrderNo = M.Test_Order(Broker,Product,BS,'0',str(Qty),'IOC','MKT',str(DayTrade))
#     print(OrderNo)
    
#     ## 判斷是否 "委託" 成功
#     #if OrderNo != '委託失敗':
#     if OrderNo[:4]=='SNVS':
#         while True:
#             # 取得 "成交" 帳務
#             #MatchInfo=GOC.MatchAccount(Broker,OrderNo)
#             MatchInfo=M.Test_MatchAccount(Broker,OrderNo)
#             # 判斷是否 "成交":
#             if len(MatchInfo[0].split(','))>1:
#                 # 成交則回傳
#                 return MatchInfo[0].split(',')
#     else:
#         return False
            

            
# # 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
# #def OrderRangeMKT(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10):
# def OrderRangeMKT(Broker,Product,BS, Qty,DayTrade='0',OrderPriceLevel=3,Wait=10):
# #def RangeMKT(Broker,Product,BS,Price,Qty,DayTrade,n):
#     # 新增訂閱要下單的商品，預防沒有取到該商品報價
#     # GOC.AddQuote(Broker,Product,True)
    
#     ## 取得委託商品的上下五檔來進行限價委託(這邊預設下單與報價使用同一個券商，若不同則需另外調整)
#     #UpdnInfo=GOQ.SubscribeLast(Broker,'updn5',Product)
#     MatchTotalQty = 0
#     MatchInfo = []
#     UpdnInfo=a.SubscribeLast(Broker,'updn5',Product)
#     # print("上下五檔: ",UpdnInfo)
#     # '''
#     # 上下五檔:  ['2019/07/31 08:58:00.53', 'MXFH9', '10710', '1', '10709', '57', '10708', '92', '10707', '98', '10706', '96', '10711', '40', '10712', '111', '10713', '102', '10714', '130', '10715', '127']
    
#     # '''
    
#     # 如果是買單，則掛上 "OrderPriceLevel" 檔委託
#     if BS == 'B':
#         OrderPoint=UpdnInfo[10+OrderPriceLevel*2]
#     # 如果是賣單，則掛下 "OrderPriceLevel" 檔委託
#     elif BS == 'S':
#         OrderPoint=UpdnInfo[OrderPriceLevel*2]
#     # 送出交易委託
#     #print([Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType])
#     #print([Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade)])
#     #OrderNo=GOC.Order(Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType )
#     OrderNo=M.Test_Order(Broker,Product,BS,str(OrderPoint),str(Qty),'ROD','LMT',str(DayTrade))
#     #print(OrderNo)   ##沒有委託成功時, 出現  "Error"
#     # 設定刪單時間
#     EndTime=time.time()+Wait
#     ## 判斷是否委託成功:
#     #if OrderNo != '委託失敗':
#     if OrderNo[:4]=='SNVS':
#         print('委託成功, 尚未成交 !')
#         print()
#         # 若大於刪單時間則跳出迴圈
#         while time.time() < EndTime and MatchTotalQty < float(Qty):
#             ## 取得成交帳務
#             #MatchInfo=GOC.MatchAccount(Broker,OrderNo)
#             MatchInfo = []
#             MatchTotalQty = 0
#             MatchInfo=M.Test_MatchAccount(Broker,OrderNo)
#             if MatchInfo != [''] :
#                for i in MatchInfo:
#                   #print('i:',i, 'MatchTotalQty:', MatchTotalQty)
#                   MatchTotalQty=MatchTotalQty + float(i.split(',')[5])
#             #print('總成交口數: ', MatchTotalQty, '委託口數: ', Qty)
#             ## 判斷是否成交:
#             #if MatchInfo != [''] :    #len(MatchInfo[0].split(','))>1 :
#                 # 成交則回傳
#                 #print('成交')
#                 #print('MatchInfo:', MatchInfo)   # ['SNVS:113,N,MXFD1,Sell,16456,1,ROD,2021-03-31 10:30:55.11,T0001,1']
#                 #return MatchInfo   #MatchInfo[0].split(',')   # ['SNVS:113','N','MXFD1','Sell','16456','1','ROD','2021-03-31 10:30:55.11','T0001','1']
#             # 稍等0.5秒
#             time.sleep(0.5)
#             #print('尚未成交')
#         MatchInfo=M.Test_MatchAccount(Broker,OrderNo)   ## MatchInfo: ['SNVS:113,N,MXFD1,Sell,16456,1,ROD,2021-03-31 10:30:55.11,T0001,1']
#         if MatchInfo != [''] :
#            print('成交 ! 輸出最新成交資料(沒有刪單): ', MatchInfo)
#            print()
#            return MatchInfo
#         # 刪單並確認委託成功刪除
#         #GOC.Delete(Broker,OrderNo)
#         #GOC.GetAccount(Broker,OrderNo)
#         M.Test_Delete(Broker,OrderNo) 
#         #M.Test_GetAccount((Broker,OrderNo)) ## M.Test_Delete(Broker,OrderNo)指令已經刪除 "OrderNo", 因此此處查詢 "OrderNo" 的帳戶資料會錯誤 
#         print('到期刪單 (委託成功, 但是完全沒有成交)')
#         print()
#         return False
#     else:
#         print('委託失敗')   ## 雖然有使用下面的 "RangeMKTDeal()" 函數給 3 次委託機會, 但每一次在委託當下沒有成功, 就立刻退出此函數. 應該給等待時間. 即使 240th 的程式中下單是使用"ROD", 也會立刻退出: "OrderNo=M.Test_Order(Broker,Product,BS,str(OrderPoint),str(Qty),'ROD','LMT',str(DayTrade))" 
#         print()
#         return False  ## 雖然有使用下面的 "RangeMKTDeal()" 函數給 3 次委託機會, 但每一次在委託當下沒有成功, 就立刻退出此函數(因為return 了). 應該給等待時間. 即使 240th 的程式中下單是使用"ROD", 也會立刻退出: "OrderNo=M.Test_Order(Broker,Product,BS,str(OrderPoint),str(Qty),'ROD','LMT',str(DayTrade))"

# # 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
# #def RangeMKTDeal(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10):
# def RangeMKTDeal(Broker,Product,BS, Qty,DayTrade='0',OrderPriceLevel=3,Wait=10):
#     # 防止例外狀況，最多下三次單
#     for i in range(3):
#         #OrderInfo=OrderRangeMKT(Broker,Product,BS,Qty,DayTrade,OrderType,OrderPriceLevel,Wait)
#         OrderInfo=OrderRangeMKT(Broker,Product,BS,Qty,DayTrade,OrderPriceLevel,Wait)
#         if OrderInfo != False:
#             return OrderInfo
#     # 三次委託皆失敗，建議當日不做交易
#     return False


