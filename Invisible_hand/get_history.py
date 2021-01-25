#!/usr/bin/env python
# coding: utf-8

# In[1]:


#调包
import matplotlib.pyplot as plt
import tushare as ts
import csv
import pandas
import datetime
import os

#初始化
ts.set_token('6996f4e55afd53fefa8c4caa9e89c4c097e772e72552c25b517f5b3c')
pro = ts.pro_api()

def getHistory(name,number,exchange,start,end):
    #获取并储存所有股票基本信息
    print('正在获取所有股票信息...')
    data = pro.stock_basic(exchange='', list_status='L', 
                           fields='ts_code,symbol,name,area,industry,list_date')
    #dateToday = datetime.datetime.today().strftime('%Y%m%d')
    file = r'C:\Users\Dell\Desktop\Invisible_hand\data.csv'
    if os.path.exists(file):
        history = pandas.read_csv(file,index_col=0)
        data.append(history)
    data.to_csv(file)
    print('已储存所有股票的基本信息！\n')
    
    #从网上获取历史数据
    print('正在获取' + name + number + '的数据...')
    stockHistory = pro.daily(ts_code=number + exchange, start_date=start, end_date=end)
    #如果已有股票数据，则直接导入新数据
    filename = r'C:\Users\Dell\Desktop\Invisible_hand\stock_prize_history' + '/' + name + number + '.csv'
    if os.path.exists(filename):
        existedHistory = pandas.read_csv(filename,index_col=0)
        stockHistory.append(existedHistory)
    #存储数据
    stockHistory.to_csv(filename)
    print(name + number + '数据已保存！\n')
    
    #读取文件数据
    with open(filename) as f:
        reader = csv.reader(f)
        rows=[row for row in  reader] 
    highs = []
    lows = []
    for row in rows:
        try:
            highs.append(float(row[4]))
            lows.append(float(row[5]))
        except:
            pass
    print('正在计算...\n')

    #计算价差大于0.02的日子有多少
    days = 0
    for i in range(0,len(highs)):
        wave = (highs[i] - lows[i])/lows[i]
        if wave >= 0.02:
            days += 1
    print('总交易天数：' + str(len(highs)))
    print('波动超过2%天数：' + str(days)+'\n')
    
    #计算总宽度
    print('在所选时间里面股票的总宽度为：（' + str(min(lows)) + str(max(highs)) + '）.\n')

    #计算各个区间段内运行的时间
    period_1 = 0
    period_2 = 0
    period_3 = 0
    period_4 = 0
    highMax = max(highs)
    highMin = min(highs)
    delta = (highMax-highMin)/4
    for high in highs:
        periodJug = (high-highMin)/delta
        if periodJug<1:
            period_1 += 1
            continue
        elif periodJug<2:
            period_2 += 1
            continue
        elif periodJug<3:
            period_3 += 1
            continue
        else:
            period_4 += 1
    print('第一区间范围：（' + str(highMin) + ',' + str(highMin+delta) + ')')
    print('最高值在第一区间内波动天数：' + str(period_1)+'\n')
    print('第二区间范围：（' + str(highMin + delta) + ',' + str(highMin+delta*2) + ')')
    print('最高值在第二区间内波动天数：' + str(period_2)+'\n')
    print('第三区间范围：（' + str(highMin + delta*2) + ',' + str(highMin+delta*3) + ')')
    print('最高值在第三区间内波动天数：' + str(period_3)+'\n')
    print('第四区间范围：（' + str(highMin + delta*3) + ',' + str(highMin+delta*4) + ')')
    print('最高值在第四区间内波动天数：' + str(period_4)+'\n')
    print('计算完成！')
    
    #将这次的数据写入文件
    print('正在保存计算结果...')
    resultFile = r'C:\Users\Dell\Desktop\Invisible_hand\result.csv'
    with open(resultFile,'a') as f:
        write=csv.writer(f)
        row = [name]
        write.writerow(row)
        row = ['时间',start,end]
        write.writerow(row)
        row = ['总宽度',min(lows),max(highs)]
        write.writerow(row)
        row=['总交易天数',len(highs)]
        write.writerow(row)
        row=['波动超过2%天数',days]
        write.writerow(row)
        row=['第一区间范围',highMin,highMin+delta]
        write.writerow(row)
        row=['最高值在第一区间内波动天数',period_1]
        write.writerow(row)
        row=['第二区间范围',highMin+delta,highMin+delta*2]
        write.writerow(row)
        row=['最高值在第二区间内波动天数',period_2]
        write.writerow(row)
        row=['第三区间范围',highMin+delta*2,highMin+delta*3]
        write.writerow(row)
        row=['最高值在第三区间内波动天数',period_3]
        write.writerow(row)
        row=['第四区间范围',highMin+delta*3,highMin+delta*4]
        write.writerow(row)
        row=['最高值在第四区间内波动天数',period_4]
        write.writerow(row)
        row = [' ']
        write.writerow(row)
    print("计算结果保存完毕！")

