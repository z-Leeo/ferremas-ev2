// API website : https://www.exchangerate-api.com/docs/overview

// Fetch exchange rate from the API
function fetchExchangeRate(baseCurrency, targetCurrency, callback) {
  fetch(`https://v6.exchangerate-api.com/v6/07c7436812f210f455d48d84/latest/${baseCurrency}`)
    .then(response => response.json())
    .then(data => {
      const rate = data.conversion_rates[targetCurrency];
      callback(rate);
    })
    .catch(error => {
      console.error('Error fetching exchange rate:', error);
      callback(null);
    });
}

function updatePrices() {
  const baseCurrency = 'USD';
  const targetCurrency = document.getElementById('currency-selector').value;
  
  fetchExchangeRate(baseCurrency, targetCurrency, function(rate) {
    if (rate !== null) {
      document.querySelectorAll('.price').forEach(function(priceElement) {
        const basePrice = parseFloat(priceElement.getAttribute('data-price'));
        const convertedPrice = (basePrice * rate).toFixed(2);
        priceElement.textContent = `${targetCurrency} $${convertedPrice}`;
      });

      let totalCarrito = 0;

      document.querySelectorAll('.total').forEach(function(totalElement) {
        const baseTotal = parseFloat(totalElement.getAttribute('data-total'));
        const convertedTotal = (baseTotal * rate).toFixed(2);
        totalElement.textContent = `${targetCurrency} $${convertedTotal}`;
        totalCarrito += parseFloat(convertedTotal);
      });

      const totalCarritoElement = document.getElementById('total-carrito');
      totalCarritoElement.textContent = `${totalCarrito.toFixed(2)}`;
    }
  });
}

document.getElementById('currency-selector').addEventListener('change', updatePrices);

// Initial call to set the prices on page load
updatePrices();
