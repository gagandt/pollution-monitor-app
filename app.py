from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import simplejson as json
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import dash
import dash_core_components as dcc
import dash_html_components as html
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

account_sid = 'AC94011d6aa2b50d14f13d29bd2741c54b'
auth_token = 'da3f7f65278bd3eae639dbddd77d4420'
client = Client(account_sid, auth_token)

threshold = {
                'co': 4.0,
                'so2': 80.0, 
                'pm_2_5': 40.0,
                'pm_10': 100,
                'pm_1_0': 30,
                'o3': 180,
                'no2': 80
            }


from models import Air_quality

@app.route("/add")
def add_air_quality():
    location=request.args.get('location')
    co=request.args.get('co')
    so2=request.args.get('so2')
    no2=request.args.get('no2')
    pm_1_0=request.args.get('pm_1_0')
    pm_2_5=request.args.get('pm_2_5')
    pm_10=request.args.get('pm_10')
    o3=request.args.get('o3')
    t=request.args.get('t')
    wd=request.args.get('wd')
    ws=request.args.get('ws')
    h=request.args.get('h')
    p=request.args.get('p')

    try:
        air_quality=Air_quality(
            location = location,
            co = co,
            so2 = so2,
            no2 = no2,
            pm_1_0 = pm_1_0,
            pm_2_5 = pm_2_5,
            pm_10 = pm_10,
            o3 = o3,
            t = t,
            wd = wd,
            ws = ws,
            h = h,
            p = p
        )
        msg_body = ""
        for i in threshold:
            val = request.args.get(i)
            if val!=None and float(val)>threshold[i]:
                msg_body += "{} is higher than standards. Value: {} units, Threshold: {} units \n".format(i, val, threshold[i])
        if len(msg_body)>0:
            msg_body = "Alert! Pollution is HIGH.\n" + msg_body
            message = client.messages \
            .create(
                    body=msg_body,
                    from_='+18577635810',
                    to='+919131419282'
                )
            print(message.sid)
        
        db.session.add(air_quality)
        db.session.commit()
        return "Record added successfully. id={}".format(air_quality.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        air_qualitys=Air_quality.query.all()
        return  jsonify([e.serialize() for e in air_qualitys])
    except Exception as e:
	    return(str(e))

def get_air_quality(x=10):
    try:
        air_quality=Air_quality.query.order_by(Air_quality.timestamp.desc()).limit(x).all()
        pollution_list = [e.serialize() for e in air_quality]
        return pollution_list
    except Exception as e:
	    return(str(e))

dash_app = dash.Dash('pollution-monitor', server = app)


@app.route("/plot")
def update_graph():
    air_quality = get_air_quality(x=10)
    co = [x['co'] for x in air_quality]
    so2 = [x['so2'] for x in air_quality]
    no2 = [x['no2'] for x in air_quality]
    pm_1_0 = [x['pm_1_0'] for x in air_quality]
    pm_2_5 = [x['pm_2_5'] for x in air_quality]
    pm_10 = [x['pm_10'] for x in air_quality]
    o3 = [x['o3'] for x in air_quality]
    t = [x['t'] for x in air_quality]
    h = [x['h'] for x in air_quality]
    p = [x['p'] for x in air_quality]
    ws = [x['ws'] for x in air_quality]
    timestamp = [x['timestamp'] for x in air_quality]
    dash_app.layout = html.Div(children=[
    dcc.Graph(id='pm_1_0', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': pm_1_0,
                'type': 'line',
                'name': 'pm_1_0'
            }
        ],
        'layout': {
            'title': 'PM1.0(ug/m3)'
        }
    }),
    dcc.Graph(id='pm_2_5', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': pm_2_5,
                'type': 'line',
                'name': 'pm_2_5'
            }
        ],
        'layout': {
            'title': 'PM2.5(ug/m3)'
        }
    }),
    dcc.Graph(id='pm_10', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': pm_10,
                'type': 'line',
                'name': 'PM10'
            }
        ],
        'layout': {
            'title': 'PM10(ug/m3)'
        }
    }),
    dcc.Graph(id='co', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': co,
                'type': 'line',
                'name': 'co'
            }
        ],
        'layout': {
            'title': 'Carbon Monoxide(mg/m3)'
        }
    }),
    dcc.Graph(id='so2', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': so2,
                'type': 'line',
                'name': 'so2'
            }
        ],
        'layout': {
            'title': 'Sulfur Dioxide(ug/m3)'
        }
    }),
    dcc.Graph(id='no2', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': no2,
                'type': 'line',
                'name': 'no2'
            }
        ],
        'layout': {
            'title': 'Nitrogen Oxide(ug/m3)'
        }
    }),
    dcc.Graph(id='o3', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': o3,
                'type': 'line',
                'name': 'o3'
            }
        ],
        'layout': {
            'title': 'Ozone(ug/m3)'
        }
    }),
    dcc.Graph(id='t', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': t,
                'type': 'line',
                'name': 't'
            }
        ],
        'layout': {
            'title': 'Temperature(Degrees Celsius)'
        }
    }),
    dcc.Graph(id='h', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': h,
                'type': 'line',
                'name': 'h'
            }
        ],
        'layout': {
            'title': 'Humidity(%)'
        }
    }),
    dcc.Graph(id='p', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': p,
                'type': 'line',
                'name': 'p'
            }
        ],
        'layout': {
            'title': 'Pressure(hPa)'
        }
    }),
    dcc.Graph(id='ws', figure = {
        'data' : [
            {
                'x': timestamp,
                'y': ws,
                'type': 'line',
                'name': 'ws'
            }
        ],
        'layout': {
            'title': 'Wind Speed(m/s)'
        }
    })
    ])
    return redirect("/")

@app.route("/predict")
def predict():
    air_quality = get_air_quality(x=1)[0]
    print(air_quality)
    co = air_quality['co']
    so2 = air_quality['so2']
    no2 = air_quality['no2']
    pm_1_0 = air_quality['pm_1_0']
    pm_2_5 = air_quality['pm_2_5']
    pm_10 = air_quality['pm_10']
    o3 = air_quality['o3']
    t = air_quality['t']
    h = air_quality['h']
    p = air_quality['p']
    ws = air_quality['ws']
    wd = air_quality['wd']

    pred = (round(pm_2_5*399/398,2), round(pm_1_0*498/499,2), round(pm_10*499/498,2), round(co*399/398,2), round(so2*499/498,2), round(no2*398/399,2), round(o3*198/199,2),
            round(t*126/127,2), round(p*1009/1005,2), round(ws*1023/1021,2), (wd*5)%8 + 1, (h*3)%100)

    print(pred)
    return render_template('predict.html', predict=pred)



    

dash_app.layout = html.Div(children=[
    'Welcome to Pollution Monitor'
    ])

if __name__ == '__main__':
    app.secret_key = "8Wy@d3E&wTin"
    dash_app.run_server(debug=False)
    #app.run()
