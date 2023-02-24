import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go

st.markdown(
    f"""
       <style>
       .stApp {{
           background-image: url("https://wallpapers.com/images/hd/hd-bitcoin-photography-xzl1ha675651mmpr.jpg");
           background-attachment: fixed;
           background-size: cover;
           /* opacity: 0.3; */
       }}
       </style>
       """,
    unsafe_allow_html=True
)
font_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 24px;
}
</style>
"""

st.write(font_css, unsafe_allow_html=True)
cl1,cl2,cl3,cl4,cl5 = st.tabs(['Main','Bitcoin Price Prediction','Record BTC','Creator of bitcoin','Download'])

with cl1:
    st.title("ยินดีต้อนรับสู่โลกของ Bitcoin🪙")
    st.write('🕛Bitcoin จะราคาเท่าไหร่(คาดการณ์)')
    st.write('🪙Bitcoin คือ?')
    st.write('🕵️‍♀️‍ไครสร้าง Bitcoin')
    st.write('⬇Download')

with cl2:


    # ดาวน์โหลดข้อมูลจาก Yahoo Finance API
    df = yf.download('BTC-USD', start='2010-01-01', end='2023-02-24')
    df.to_csv('BTC-USD.csv')
    df = df.reset_index()

    # Create a new column for the target variable (price after 30 days)
    df['Price_After_30_Days'] = df['Close'].shift(-30)

    # วางแถวที่มีค่าขาดหายไป
    df = df.dropna()

    # สร้างคุณสมบัติและตัวแปรเป้าหมาย
    X = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']]
    y = df['Price_After_30_Days']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # สร้างแบบจำลองการถดถอยเชิงเส้น
    model = LinearRegression()

    # ฝึกโมเดล
    model.fit(X_train, y_train)


    # สร้างฟังก์ชั่นทำนายราคาซื้อขาย Bitcoin
    def predict_price(high, low, open, volume, adj_close):
        prediction = model.predict([[high, low, open, volume, adj_close]])
        return prediction[0]


    # สร้างชื่อสำหรับแอป
    st.title('อนาคต Bitcion จะราคาเท่าไหรนะ?')

    # สร้างกล่องอินพุตสำหรับการป้อนข้อมูลของผู้ใช้
    high = st.number_input('High')
    low = st.number_input('Low')
    open = st.number_input('Open')
    volume = st.number_input('Volume')
    adj_close = st.number_input('Adj Close')

    # สร้างปุ่มเพื่อทำการทำนาย
    if st.button('Predict Price'):
        result = predict_price(high, low, open, volume, adj_close)
        st.header('The predicted price for Bitcoin after 30 days is $ {:.2f}'.format(result))



    # แสดงภาพข้อมูล
    st.header('Data Visualization')
    st.line_chart(df['Close'])



    # ภาพราคาที่คาดการณ์ไว้
    st.header('Predicted Price Visualization')
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Close'], label='Actual Price')
    ax.plot(df['Date'], model.predict(X), label='Predicted Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    st.pyplot(fig)



    # พิมพ์รูปทรงชุดฝึกและชุดทดสอบ
    print(X_train.shape)  # Should print (num_samples, num_features)
    print(X_test.shape)  # Should print (num_samples, num_features)



    # Print the names of features
    print(X_train.columns)
    print(X_test.columns)

    # Set the title of the web app
    st.title('Real-time BTC Price Chart')

    # Set the start and end dates for the chart data
    start_date = pd.to_datetime('2021-01-01')
    end_date = pd.to_datetime('now')

    # Download the BTC price data
    df = yf.download('BTC-USD', start=start_date, end=end_date)

    # Create the candlestick chart
    candlestick = go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'])

    # Set the layout of the chart
    layout = go.Layout(title='BTC Price Chart',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'))

    # Combine the data and layout into a Figure object
    fig = go.Figure(data=[candlestick], layout=layout)

    # Add the chart to the web app
    st.plotly_chart(fig, use_container_width=True)

    # Add a link to the data source
    st.write('Data Source: Yahoo git initFinance')



with cl3:
    st.title('Bitcoin คืออะไร?')
    st.write('Bitcoin คืออะไร?: รวมเรื่องต้องรู้ ก่อนลงทุนบิตคอยน์')
    st.image('https://scontent.finnomena.com/sites/1/2022/03/fe4f4c04-bitcoin-01.jpg')
    st.text_area( '''
        บิตคอยน์ (Bitcoin) หรือ BTC คือสกุลเงินดิจิทัล (Cryptocurrency) สกุลแรกของโลกที่ถูกสร้างขึ้นบน “บล็อกเชน” (Blockchain) ซึ่งเป็นเทคโนโลยีที่ใช้สำหรับตรวจสอบธุรกรรมใด ๆ ที่เกี่ยวข้องกับบิตคอยน์ หัวใจของบิตคอยน์คือ “การกระจายศูนย์” (Decentralized) ที่ปราศจากการควบคุมจากตัวกลางหรือการกำกับดูแลของรัฐบาลและธนาคารใด ๆ

ธุรกรรมที่เกี่ยวข้องกับบิตคอยน์แต่ละรายการถูกบันทึกไว้ในบัญชีแยกประเภทแบบกระจายศูนย์  ทำให้ธุรกรรมใด ๆ ยากที่จะย้อนกลับ ดัดแปลง หรือทำลายทิ้ง

ปัจจุบันบิตคอยน์มีมูลค่าและส่วนแบ่งตลาดสูงที่สุดในตลาดคริปโตฯ ด้วยปริมาณการซื้อขายอย่างมหาศาลในแต่ละวัน

จำนวนบิตคอยน์มีอยู่จำกัดที่ประมาณ 21 ล้านเหรียญ ซึ่งล่าสุด ณ เดือนกุมภาพันธ์ 2022 บิตคอยน์ถูกขุดไปแล้วกว่า 18.97 ล้านเหรียญ หรือราว 90% ของจำนวนบิตคอยน์ทั้งหมด โดยคาดว่าบิตคอยน์จะถูกขุดหมดประมาณปี 2140, (...)
        
        
        
        บิตคอยน์ (อังกฤษ: Bitcoin) เป็นคริปโทเคอร์เรนซี[10]:3 บิตคอยน์เป็นสกุลเงินดิจิทัลแรกที่ใช้ระบบกระจายอำนาจ โดยไม่มีธนาคารกลางหรือแม้แต่ผู้คุมระบบแม้แต่คนเดียว[10]:1[11] เครือข่ายเป็นแบบเพียร์ทูเพียร์ และการซื้อขายเกิดขึ้นระหว่างจุดต่อเครือข่าย (network node)โดยตรง ผ่านการใช้วิทยาการเข้ารหัสลับและไม่มีสื่อกลาง[10]:4 การซื้อขายเหล่านี้ถูกตรวจสอบโดยรายการเดินบัญชีแบบสาธารณะที่เรียกว่าบล็อกเชน บิตคอยน์ถูกพัฒนาโดยคนหรือกลุ่มคนภายใต้นามแฝง "ซาโตชิ นากาโมโตะ"[12] และถูกเผยแพร่ในรูปแบบซอฟต์แวร์โอเพนซอร์ซในปี พ.ศ. 2552[13]

บิตคอยน์ถูกสร้างขึ้นใหม่ด้วย 'การขุด' (mining, การทำเหมือง) และสามารถแลกเป็นสกุลเงินอื่น[14] สินค้า และบริการ ณ เดือนกุมภาพันธ์ พ.ศ. 2558 มีร้านค้ากว่า 100,000 ร้านยอมรับการจ่ายเงินด้วยบิตคอยน์[15] งานวิจัยจากมหาวิทยาลัยเคมบริดจ์ประมาณว่าใน พ.ศ. 2560 มีผู้ใช้เงินตราแบบดิจิทัล 2.9 ถึง 5.8 ล้านคน โดยส่วนใหญ่แล้วใช้บิตคอยน์


คำว่า บิตคอยน์ ปรากฏขึ้นครั้งแรกและถูกให้ความหมายในสมุดปกขาว (white paper)[4] ที่ถูกตีพิมพ์เมื่อวันที่ 31 ตุลาคม พ.ศ. 2551[17] เป็นการรวมคำว่า บิต และ คอยน์ เข้าด้วยกัน[18]

หน่วย
หน่วยของบัญชีระบบบิตคอยน์คือ บิตคอยน์ จนถึง ค.ศ. 2014 ชื่อที่ใช้ในการซื้อขาย (ticker symbol) ของบิตคอยน์ได้แก่ BTC[a] และ XBT[b] โดยมีสัญลักษณ์ยูนิโคด ₿[23]:2 หน่วยย่อยที่มักถูกใช้ได้แก่ มิลลิบิตคอยน์ (mBTC) และ ซาโตชิ ซึ่งเป็นชื่อที่ตั้งตามผู้สร้างบิตคอยน์ ซาโตชิเป็นหน่วยย่อยที่เล็กที่สุดแสดงจำนวน 0.00000001 บิตคอยน์ หรือ หนึ่งในร้อยล้านของบิตคอยน์[2] ส่วนมิลลิบิตคอยน์เท่ากับ 0.001 บิตคอยน์ หรือ หนึ่งในพันของบิตคอยน์ และยังเท่ากับ 100,000 ซาโตชิ[24]

ในวันที่ 18 สิงหาคม พ.ศ. 2551 ชื่อโดเมน "bitcoin.org" ถูกตั้งขึ้น[25] ในเดือนพฤศจิกายนปีเดียวกัน ลิงก์ไปยังเอกสารในหัวข้อ บิตคอยน์:ระบบเงินอิเลคโทรนิคแบบเพียร์ทูเพียร์[4] เขียนโดย ซาโตชิ นากาโมโตะ ได้ถูกส่งไปยังกลุ่มรายชื่อของอีเมลของวิทยาการเข้ารหัสลับ[25] นากาโมโตะนำซอฟต์แวร์บิตคอยน์มาใช้เป็นโค้ดแบบโอเพนซอร์ซและเปิดตัวในเดือนมกราคม พ.ศ. 2552[26][13] ขณะนั้นจนถึงตอนนี้ตัวตนของนากาโมโตะยังไม่ถูกเปิดเผย[27]

ในเดือนมกราคม พ.ศ. 2552 เครือข่ายบิตคอยน์ถือกำเนิดขึ้นหลัง ซาโตชิ นากาโมโตะ เริ่มขุดบล็อกแรกของเชนที่เรียกว่า บล็อกกำเนิด ที่ให้รางวัลจำนวน 50 บิตคอยน์[28][29]

หนึ่งในผู้สนับสนุน ผู้นำไปใช้ และผู้ร่วมพัฒนาบิตคอยน์คนแรก ๆ เป็นผู้รับการซื้อขายบิตคอยน์ครั้งแรก เขาเป็นโปรแกรมเมอร์ที่ชื่อว่า ฮาล ฟินนีย์ (Hal Finney) ฟินนีย์ดาวน์โหลดซอฟต์แวร์บิตคอยน์ในวันแรกที่เปิดตัว และได้รับ 10 บิตคอยน์จากนากาโมโตะในการซื้อขายบิตคอยน์ครั้งแรกของโลก[30][31] ผู้สนับสนุนแรกเริ่มคนอื่น ๆ ได้แก่ Wei Dai ผู้สร้าง b-money และ Nick Szabo ผู้สร้าง bit gold ทั้งคู่ที่มาก่อนบิตคอยน์[32]

ในช่วงแรก มีการประมาณว่านากาโมโตะได้ทำการขุดจำนวน 1 ล้านบิตคอยน์[33] ในพ.ศ. 2553 นากาโมโตะส่งต่อกุญแจเตือนเครือข่ายและการควบคุมที่เก็บโค้ดหลักบิตคอยน์ (Bitcoin Core code) ให้กับ Gavin Andresen ผู้ที่ต่อมากลายเป็นหัวหน้านักพัฒนาหลักของมูลนิธิบิตคอยน์ (Bitcoin Foundation)[34][35] จากนั้นนากาโมโตะก็เลิกยุ่งเกี่ยวกับบิตคอยน์[36] จากนั้น Andresen ตั้งเป้าหมายว่าจะกระจายอำนาจการควบคุม และกล่าวว่า "หลังซาโตชิถอยออกไปและโยนโครงการมาบนไหล่ของฉัน สิ่งแรกที่ฉันทำคือการพยายามกระจายอำนาจ เพื่อที่โครงการจะไปต่อได้ แม้หากฉันโดนรถบัสชนก็ตาม"[36]

มูลค่าของการแลกเปลี่ยนบิตคอยน์ครั้งแรกถูกต่อรองผ่านทางเว็บบอร์ดพูดคุยบิตคอยน์ โดยมีการซื้อขายครั้งหนึ่งที่ใช้ 10,000 BTC เพื่อซื้อพิซซ่าจำนวนสองถาดแบบอ้อมจาก Papa John's[28]

เมื่อวันที่ 6 สิงหาคม พ.ศ. 2553 ช่องโหว่ครั้งใหญ่ในโพรโทคอลของบิตคอยน์ถูกพบ การซื้อขายไม่ได้ถูกตรวจสอบอย่างถูกต้องก่อนถูกใส่เข้าไปในบล็อกเชน ทำให้ผู้ใช้สามารถเลี่ยงข้อจำกัดทางเศรษฐศาสตร์ของบิตคอยน์ และสร้างบิตคอยน์ขึ้นมาได้ในจำนวนไม่จำกัด[37][38] ในวันที่ 15 สิงหาคม ช่องโหว่นี้ถูกใช้สร้างกว่า 184 ล้านบิตคอยน์ผ่านการซื้อขายหนึ่งครั้ง และส่งไปยังที่อยู่สองที่ในเครือข่าย การซื้อขายถูกพบภายในไม่กี่ชั่วโมง และถูกลบออกจากบันทึกหลังแก้ไขบัคและอัปเดตรุ่นโพรโทคอลของบิตคอยน์[39][37][38]

เมื่อวันที่ 1 สิงหาคม พ.ศ. 2560 ฮาร์ดฟอร์ค (hard fork) ของบิตคอยน์ถูกสร้างขึ้น เรียกว่า บิตคอยน์แคช (Bitcoin Cash) บิตคอยน์แคชมีข้อจำกัดของขนาดบล็อกที่ใหญ่ขึ้นและมีบล็อกเชนที่เหมือนกัน ณ เวลาฟอร์ค
''')



with cl4:


    st.title('แล้วไครเป็นคนสร้าง Bitcion')
    st.image('https://scontent.finnomena.com/sites/1/2022/03/0247c6a1-bitcoin-02.jpg')
    st.title('“ซาโตชิ นากาโมโตะ”')

with cl5:
    st.title('download ข้อมูลได้ที่นี้')