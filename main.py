import yfinance as yf
import pandas as pd
import requests
import time

# ⚙️ CONFIGURACIÓN GENERAL
activos = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'AMZN']
periodo_ma = 50             # Puedes cambiar a 200, etc.
tipo_ma = 'SMA'             # O 'EMA'
tolerancia = 0.5            # Diferencia aceptable
intervalo = '1h'            # '1m', '5m', '15m', '1h', '1d'

# 🔔 TELEGRAM
TELEGRAM_TOKEN = '7996693761:AAEorUumnpmWSXdVwmJBfYdIqdoA96DCaBk'
TELEGRAM_CHAT_ID = '1724546632'

def enviar_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error al enviar mensaje de Telegram: {e}")

def comprobar_toques():
    for symbol in activos:
        try:
            # Descargar datos
            df = yf.download(symbol, period='30d', interval=intervalo, auto_adjust=False, progress=False)

            df = df.dropna()

            # Calcular media móvil
            if tipo_ma == 'SMA':
                df['MA'] = df['Close'].rolling(periodo_ma).mean()
            elif tipo_ma == 'EMA':
                df['MA'] = df['Close'].ewm(span=periodo_ma).mean()
            else:
                print(f"{symbol}: Tipo de media móvil desconocido.")
                continue

            # Obtener último precio y media
            precio_actual = df['Close'].iloc[-1].item()
            ma_actual = df['MA'].iloc[-1].item()
            # Verificar si hay datos suficientes
            if pd.isna(ma_actual):
                print(f"{symbol}: No hay suficientes datos para calcular la media móvil.")
                continue

            # Mostrar en consola
            print(f"{symbol}: Precio = {precio_actual:.2f}, MA = {ma_actual:.2f}")

            # Verificar si toca la media
            if abs(precio_actual - ma_actual) <= tolerancia:
                mensaje = f"🔔 {symbol} ha tocado la media {tipo_ma} {periodo_ma}: Precio={precio_actual:.2f}, MA={ma_actual:.2f}"
                enviar_telegram(mensaje)

        except Exception as e:
            print(f"Error en {symbol}: {e}")

# 🔁 BUCLE INFINITO (cada hora)
while True:
    comprobar_toques()
    time.sleep(3600)
