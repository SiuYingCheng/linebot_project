# 週末外游導航 APP

## 前言：
週末是人們難得休閑的日子，但因爲前五天的工作忙碌，導致一直沒有好好規劃週末的活動。週末外游導航 APP 的誕生是爲了解決此問題，人們可以透過 APP 查詢今日天氣，進而查詢新電影與好吃的店家，讓美食和電影陪伴著度過每一個週末。

## 環境：
python 3.8.3

## 技術
- Olami
    - 具有NLP的聊天機器人
- Beautifulsoup4
    - 爬取台灣各地美食餐廳推薦與新電影排行

## 使用教學
1. install `pipenv`
```shell
pip3 install pipenv
```
2. install 所需套件
```shell
pipenv install --three
```
3. 從`.env.sample`產生出一個`.env`，並填入以下四個資訊

- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
- Olami
    - APP_KEY
    - APP_SECRET
4. install `ngrok`
5. run `ngrok` to deploy Line Chat Bot locally
```shell
ngrok http 8000
```
6. execute app.py
```shell
python app.py
```

## 使用說明
- 基本操作:
- 以下兩個指令皆可隨時輸入
        - `choose`
            - reset所有資訊
        - `chat`
            - 切換到聊天機器人模式
 - 架構圖
    1. 輸入`choose`開始使用APP
    2. 選擇 `movie` 來查看本周電影
    3. 選擇 `picture` 來查看舒壓圖片
    4. 選擇 `show_fsm` 來查看fsm圖
    5. 選擇 `restaurant` 來查看附近餐廳
 
 ## 使用示範
 ### choose 主頁：
 ![](https://i.imgur.com/Uh4czzN.jpg)
 
 ### movie:
 ![](https://i.imgur.com/Jj2nv09.jpg)
 
 ### picture:
 ![](https://i.imgur.com/byMcjLy.jpg)
 ![](https://i.imgur.com/H91g0nb.jpg)
 ![](https://i.imgur.com/CKE9Dw9.jpg)
 ![](https://i.imgur.com/lusDXsj.jpg)
 
 ### restaurant:
 ![](https://i.imgur.com/pPayw9S.jpg)
 
 ### show-fsm:
 ![](https://i.imgur.com/2iHwcxa.jpg)
 
 ### chat:
 ![](https://i.imgur.com/GXtSiU4.jpg)
 
 ### state說明
- user: 輸入choose開始使用APP
- choose: 選擇想要的休閑活動
- movie: 顯示本週五大熱門電影
- restaurant: 顯示特定地區的有名餐廳
- picture: 顯示好笑的舒壓圖片
  - hot_boy: 顯示舒壓帥哥圖
  - hot_girl: 顯示舒壓美女圖
  - meaningful_quote: 顯示格世名言圖
- show-fsm: 顯示fsm圖
