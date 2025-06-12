import numpy as np
import os
import plotly.graph_objects as go
import scipy.ndimage

USE_MOCK_DATA = True

if USE_MOCK_DATA:
    from mock_option_data import mock_data
    data = mock_data
else:
    import requests
    os.system("TD_API_KEYS.py")
    payload = {'apikey':'-------------',
            'symbol':'TSLA',
            'contractType':'ALL'}
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"
    content = requests.get(url = endpoint, params = payload)
    data = content.json()

call_map = data['callExpDateMap']
expiries = list(call_map.keys())
strikes = sorted({float(strike) for expiry in call_map.values() for strike in expiry.keys()})

X = []
Y = []
Z = []

for strike in strikes:
    row_days = []
    row_vols = []
    for expiry in expiries:
        days = int(expiry.split(":")[1])
        row_days.append(days)
        vol = None
        if str(strike) in call_map[expiry]:
            vol = call_map[expiry][str(strike)][0]['volatility']
        else:
            vol = float('nan')
        row_vols.append(vol)
    X.append(row_days)
    Y.append([strike]*len(expiries))
    Z.append(row_vols)

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)

fig = go.Figure(data=[go.Surface(
    x=X,
    y=Y,
    z=Z,
    colorscale='Viridis',
    showscale=True,
    opacity=0.9
)])

fig.update_layout(
    title='Volatility Surface (Calls)',
    autosize=False,
    width=800,
    height=800,
    margin=dict(l=65, r=50, b=65, t=90),
    scene=dict(
        xaxis_title='Days to expiry',
        yaxis_title='Strike',
        zaxis_title='Implied Volatility',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )
)

fig.show()
