/* eslint-disable radix */
/* eslint-disable no-unused-vars */
/* eslint-disable no-console */
/* eslint-disable import/newline-after-import */

// Redis client
import redis from 'redis';
const client = redis.createClient();
const utils = require('util');

client.get = utils.promisify(client.get).bind(client);
client.set = utils.promisify(client.set).bind(client);

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// App Server
const express = require('express');
// Create an express server listening on the port 1245.
const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`Listening on port ${port}: http://localhost:${port}`);
});

// Data
const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 14,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

// Data access
function getItemById(id) {
  return listProducts.find((item) => item.itemId === parseInt(id));
}
/** Alternatively using our friendly for loop
function getItemById(id) {
  for (const product of listProducts) {
    if (product.id === id) {
      return product;
    }
  }
  // If no matching item is found, return undefined
  return undefined;
}
 * */

// Write a function reserveStockById that will take itemId and stock as arguments:
// It will set in Redis the stock for the key item.ITEM_ID
function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

// Write an async function getCurrentReservedStockById, that will take itemId as an argument:
// It will return the reserved stock for a specific itemId
async function getCurrentReservedStockById(itemId) {
  const data = await client.get(`item.${itemId}`);
  return data;
}

// Create the route GET /list_products that will return the list of every available product
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Create the route GET /list_products/:id that will return the product with the specified id
app.get('/list_products/:itemId', async (req, res) => {
  const id = req.params.itemId;
  const item = getItemById(id);
  if (item) {
    // get availble stock from redis
    const stock = parseInt(await getCurrentReservedStockById(id));
    if (stock.toString() === 'NaN') {
      item.currentQuantity = item.initialAvailableQuantity;
    } else {
      item.currentQuantity = stock;
    }
    res.json(item);
  } else {
    res.status(404).json({ status: 'Product not found' });
  }
});

// create a function reserveStockById that will take itemId and stock as arguments:
app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(itemId);
  if (!item) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }
  let currStock = parseInt(await getCurrentReservedStockById(itemId));
  if (currStock.toString() === 'NaN') {
    currStock = item.initialAvailableQuantity;
  }
  // if less than or equal to zero
  if (currStock <= 0) {
    res.status(403).json({ status: 'Not enough stock available', itemId });
    return;
  }
  // if more than zero, reserve 1 stock
  currStock -= 1;
  item.currentQuantity = currStock;
  reserveStockById(itemId, currStock);
  res.json({
    status: 'Reservation confrirmed',
    itemId,
  });
});
