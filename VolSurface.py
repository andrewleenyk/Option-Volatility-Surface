import requests
import numpy as np
import os
os.system("TD_API_KEYS.py")
#from TD_API_KEYS.py import payload
payload = {'apikey':'-------------',
        'symbol':'TSLA',
        'contractType':'ALL'}
endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"
content = requests.get(url = endpoint, params = payload)

data = content.json()

class calls:
    def daystoexpiry(alloptionsdata):
        maturities = []

        for expiry in alloptionsdata['callExpDateMap']:
            for strike in alloptionsdata['callExpDateMap'][expiry]:
                    maturities.append(int(expiry[11:]))
        return maturities
    
    def moneyness(alloptionsdata):
        arr = []

        priceUnderlying = int(alloptionsdata['underlyingPrice'])
        for expiry in alloptionsdata['callExpDateMap']:
            for strike in alloptionsdata['callExpDateMap'][expiry]:
                arr.append(strike)
        return arr

    def impliedvolatility(alloptionsdata):
        arr = []

        for expiry in alloptionsdata['callExpDateMap']:
            for strike in alloptionsdata['callExpDateMap'][expiry]:
                #arr.append((priceUnderlying-float(strike))/priceUnderlying)
                arr.append(alloptionsdata['callExpDateMap'][expiry][strike][0]['volatility'])
        return arr
    
    def delta(alloptionsdata):
        arr = []

        for expiry in alloptionsdata['callExpDateMap']:
            for strike in alloptionsdata['callExpDateMap'][expiry]:
                #arr.append((priceUnderlying-float(strike))/priceUnderlying)
                arr.append(alloptionsdata['callExpDateMap'][expiry][strike][0]['delta'])
        
        return arr

class puts:
    def daystoexpiry(alloptionsdata):
        maturities = []

        for expiry in alloptionsdata['putExpDateMap']:
            for strike in alloptionsdata['putExpDateMap'][expiry]:
                    maturities.append(int(expiry[11:]))
        return maturities
    
    def moneyness(alloptionsdata):
        arr = []

        priceUnderlying = int(alloptionsdata['underlyingPrice'])
        for expiry in alloptionsdata['putExpDateMap']:
            for strike in alloptionsdata['putExpDateMap'][expiry]:
                arr.append(strike)
        return arr

    def impliedvolatility(alloptionsdata):
        arr = []

        for expiry in alloptionsdata['putExpDateMap']:
            for strike in alloptionsdata['putExpDateMap'][expiry]:
                #arr.append((priceUnderlying-float(strike))/priceUnderlying)
                arr.append(alloptionsdata['putExpDateMap'][expiry][strike][0]['volatility'])
        return arr
    
    def delta(alloptionsdata):
        arr = []

        for expiry in alloptionsdata['putExpDateMap']:
            for strike in alloptionsdata['putExpDateMap'][expiry]:
                #arr.append((priceUnderlying-float(strike))/priceUnderlying)
                arr.append(alloptionsdata['putExpDateMap'][expiry][strike][0]['delta'])
        
        return arr
        


deltaa = calls.delta(data)
days = calls.daystoexpiry(data)
money = calls.moneyness(data)
index=0


import scipy.ndimage
depthSmooth = scipy.ndimage.filters.gaussian_filter([deltaa], [900,900])
newmmmod = np.asmatrix([days,money,depthSmooth[0]])

import plotly.graph_objects as go

fig = go.Figure(data=[go.Surface(z=newmmmod,colorscale='blackbody')])

fig.update_layout(title='Volatility Surface', autosize=False,
                width=500, height=500,
                margin=dict(l=65, r=50, b=65, t=90))
fig.update_layout(scene = dict(
                    xaxis_title='Days to expiry',
                    yaxis_title='Moneyness',
                    zaxis_title='Implied Volatility'),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))


fig.show()
