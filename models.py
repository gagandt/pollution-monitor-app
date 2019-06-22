import time
from app import db
import simplejson as json
class Air_quality(db.Model):
    __tablename__ = 'air_quality'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP)
    location = db.Column(db.String())
    co = db.Column(db.Float(4))
    so2 = db.Column(db.Float(4))
    no2 = db.Column(db.Float(4))
    pm_1_0 = db.Column(db.Float(4))
    pm_2_5 = db.Column(db.Float(4))
    pm_10 = db.Column(db.Float(4))
    o3 = db.Column(db.Float(4))
    t = db.Column(db.Float(4))
    wd = db.Column(db.Integer)
    ws = db.Column(db.Float(4))
    h = db.Column(db.Float(4))
    p = db.Column(db.Float(4))

    def __init__(self,location,co,so2,no2,pm_1_0,pm_2_5,pm_10,o3,t,wd,ws,h,p):
        time.ctime()
        self.timestamp = time.strftime('%l:%M%p %Z on %b %d, %Y')
        self.location = location
        self.co = co
        self.so2 = so2
        self.no2 = no2
        self.pm_1_0 = pm_1_0
        self.pm_2_5 = pm_2_5
        self.pm_10 = pm_10
        self.o3 = o3
        self.t = t
        self.wd = wd
        self.ws = ws
        self.h = h
        self.p = p

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'location' : self.location,
            'co': self.co,
            'so2': self.so2,
            'no2' : self.no2,
            'pm_1_0' : self.pm_1_0,
            'pm_2_5' : self.pm_2_5,
            'pm_10' : self.pm_10,
            'o3' : self.o3,
            't' : self.t,
            'wd' : self.wd,
            'ws' : self.ws,
            'h' : self.h,
            'p' : self.p
        }
