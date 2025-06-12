import random

mock_data = {
    'underlyingPrice': 250.0,
    'callExpDateMap': {},
    'putExpDateMap': {}
}

strikes = [round(220 + i * 2.5, 1) for i in range(25)]

expiries = [
    '2024-08-16:30',
    '2024-08-23:37',
    '2024-08-30:44',
    '2024-09-06:51',
    '2024-09-20:65',
    '2024-10-18:93',
    '2024-11-15:121',
    '2024-12-20:156'
]

for expiry in expiries:
    mock_data['callExpDateMap'][expiry] = {}
    mock_data['putExpDateMap'][expiry] = {}
    for strike in strikes:
        days = int(expiry.split(":")[1])
        base_vol = 0.30 + (days / 1000)
        moneyness = (strike - 250.0) / 250.0
        vol_adjust = abs(moneyness) * 0.1
        noise = random.uniform(-0.02, 0.02)
        implied_vol = base_vol + vol_adjust + noise
        implied_vol = max(0.1, min(0.5, implied_vol))
        mock_data['callExpDateMap'][expiry][str(strike)] = [{'volatility': implied_vol, 'delta': 0.5 + (moneyness * 0.5)}]
        mock_data['putExpDateMap'][expiry][str(strike)] = [{'volatility': implied_vol, 'delta': -0.5 - (moneyness * 0.5)}]

mock_data['callExpDateMap']['2024-09-20:65']['250.0'][0]['volatility'] -= 0.05
mock_data['callExpDateMap']['2024-10-18:93']['245.0'][0]['volatility'] -= 0.07

mock_data['putExpDateMap']['2024-09-20:65']['250.0'][0]['volatility'] -= 0.05
mock_data['putExpDateMap']['2024-10-18:93']['245.0'][0]['volatility'] -= 0.07
