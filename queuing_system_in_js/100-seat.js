const express = require("express");
const redis = require("redis");
const { promisify } = require("util");
const kue = require("kue");

const app = express();
const port = 1245;

// Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Kue queue
const queue = kue.createQueue();

// Available seats variables
let availableSeats = 50; // Initialize available seats
let reservationEnabled = true; // Flag to control reservation

// Function to reserve seats (Redis)
async function reserveSeat(number) {
  availableSeats = Math.max(0, availableSeats - number); // Ensure non-negative seats
  await setAsync("available_seats", availableSeats);
}

// Function to get current available seats (Redis)
async function getCurrentAvailableSeats() {
  const currentSeats = await getAsync("available_seats");
  return parseInt(currentSeats, 10) || 0;
}

// Kue job for seat reservation
function createReserveSeatJob() {
  const job = queue
    .createJob("reserve_seat")
    .on("complete", () =>
      console.log(`Seat reservation job ${job.id} completed`)
    )
    .on("failed", (err) =>
      console.error(`Seat reservation job ${job.id} failed: ${err.message}`)
    );
  job.save();
  return job;
}

// Route: GET /available_seats
app.get("/available_seats", async (req, res) => {
  const currentSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: currentSeats });
});

// Route: GET /reserve_seat
app.get("/reserve_seat", async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = createReserveSeatJob();
  res.json({ status: "Reservation in process" });

  try {
    await job.complete();
  } catch (err) {
    console.error(err);
    res.json({ status: "Reservation failed" });
  }
});

// Route: GET /process (async processing)
app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });

  try {
    const currentSeats = await getCurrentAvailableSeats();
    await reserveSeat(1);

    if (currentSeats === 0) {
      reservationEnabled = false;
    }
  } catch (err) {
    console.error(err);
  }
});

// Start Kue queue worker
queue.process("reserve_seat", async (job, done) => {
  // Simulate some processing time (optional)
  await new Promise((resolve) => setTimeout(resolve, 1000));
  done();
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
