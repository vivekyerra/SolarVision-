from flask import Flask,render_template,request
import pandas as pd
import numpy as np
df=pd.read_csv('cities_prediction.csv')

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_var=request.form['City']
        area_var=request.form['area']
        c_unit_var=request.form['unit_current']
        c_install_var=request.form['installation']
        bill_amnt_var=request.form['bill']
        report=solarVision(city_var,area_var,c_unit_var,c_install_var,bill_amnt_var)
        return render_template('report.html',head1=report)
    else:
        return render_template('index.html')
def solarVision(city,area,c_unit,c_install,bill_amnt):
    citydata=df[city]
    area=float(area)
    c_install=float(c_install)
    c_unit=float(c_unit)
    bill_amnt=float(bill_amnt)
    citydata=citydata.to_numpy()
    gen_amnt=citydata*area*c_unit
    savings=0
    months=0
    daily_bill=bill_amnt/30.5
    try:
        if daily_bill<gen_amnt[0]:
            for gen_month in gen_amnt:
                savings+=gen_month-daily_bill
                months+=1
                if savings>=c_install:
                    break
        else:
            area=bill_amnt/(citydata[0]*c_unit)
            return 'the area of the solar panels must be atleast {}sq.mts to reach breakeven'.format(area.round())
    except :
        return "It will take more than 3 years for you to reach profit"
    months=round(months/30)
    return "It will take {} months to reach breakeven.".format(months)
    

if __name__=="__main__":
    app.run(debug=True)