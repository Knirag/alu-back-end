const express = require("express");
const redis = require("redis");
const { promisify } = require("util");

const app = express();
const port = 1245;

// Sample product list
const listProducts = [
  { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

// Connect to Redis
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Function to get item by ID
function getItemById(id) {
  return listProducts.find((item) => item.id === id);
}

// Function to reserve stock for an item
async function reserveStockById(itemId, stock) {
  const key = `item.${itemId}`;
  await setAsync(key, stock);
}

// Function to get current reserved stock for an item
async function getCurrentReservedStockById(itemId) {
  const key = `item.${itemId}`;
  const reservedStock = await getAsync(key);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
}

// Route: GET /list_products
app.get("/list_products", (req, res) => {
  res.json(
    listProducts.map((item) => ({
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock,
    }))
  );
});

// Route: GET /list_products/:itemId
app.get("/list_products/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId, 10));
  if (!item) {
    return res.json({ status: "Product not found" });
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  res.json({ ...item, currentQuantity: currentStock });
});

// Route: GET /reserve_product/:itemId
app.get("/reserve_product/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId, 10));
  if (!item) {
    return res.json({ status: "Product not found" });
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === 0) {
    return res.json({ status: "Not enough stock available", itemId });
  }

  await reserveStockById(itemId, currentStock - 1);
  res.json({ status: "Reservation confirmed", itemId });
});

app.listen(port, () => console.log(`Server listening on port ${port}`));
