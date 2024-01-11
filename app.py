from flask import Flask,render_template,jsonify,request
import pickle
import sqlite3

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def prediction():
    print(request.method)
    if request.method=='POST':
        nitro=request.form.get("nitrogen")
        phs=request.form.get("phosphorous")
        k=request.form.get("potassium")
        temp=request.form.get("temperature")
        hd=request.form.get("humidity")
        ph=request.form.get("ph")
        rf=request.form.get("rainfall")
        print(nitro,phs,k,temp,hd,ph,rf)
        with open('model.pkl','rb') as model_file:
            mlmodel=pickle.load(model_file)
        res=mlmodel.predict([[float(nitro),float(phs),float(k),float(temp),float(hd),float(ph),float(rf)]])   
        print(res)
        conn = sqlite3.connect('cropdata.db')
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO CROPS VALUES({nitro},{phs},{k},{temp},{hd},{ph},{rf},'{res[0]}')''')
        conn.commit()
        return  render_template("result.html",res=res[0])
    else:
        return render_template('make-predictions.html')

@app.route('/show-data',methods =['GET','POST'])    
def showdata():
    conn = sqlite3.connect('cropdatabase.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM CROPS;')
    x = cur.fetchall()
    #print(data)
    li  = []
    for i in x:
        p = {}
        p['Nitrogen'] = i[0]
        p['Phosphorus'] = i[1]
        p['Potassium'] = i[2]
        p['Temperature'] = i[3]
        p['Humidity'] = i[4]
        p['Ph'] = i[5]
        p['Rainfall'] = i[6]
        p['Result'] = i[7]
        li.append(p)
    return render_template('showdata.html',data = li)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050)
