# En app/utils/utils.py

from django.conf import settings
import requests

def convert_currency(base_currency, target_currency):
    api_key = settings.CURRENCY_API_KEY  # Asegúrate de configurar esto en tu settings.py

    if target_currency == base_currency:
        return 1.0  # Si la moneda objetivo es la misma que la base, la tasa de cambio es 1.0

    # Llama a tu API para obtener la tasa de cambio
    url = f'https://api.yourcurrencyapi.com/convert?api_key={api_key}&from={base_currency}&to={target_currency}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'conversion_rate' in data:
            rate = data['conversion_rate']
            return rate
        else:
            print(f"API response error: {data}")
            return None

    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None


# En utils.py
def convert_currency(request, base_currency):
    # Lógica para obtener la tasa de cambio según la moneda base
    # Ejemplo básico:
    if base_currency == 'USD':
        rate = 1.0  # Tasa de cambio base
    else:
        # Lógica para obtener la tasa de cambio desde una API o base de datos
        # Aquí debes implementar la lógica específica para tu aplicación
        rate = 0.0  # Aquí deberías calcular la tasa de cambio real

    return rate
