/* eslint-disable prefer-const */
/* eslint-disable max-len */
/* eslint-disable radix */
/* eslint-disable no-unused-vars */
/* eslint-disable no-console */
/* eslint-disable import/newline-after-import */

// Redis
// Create a Redic client:
// Redis client
import redis from 'redis';
const utils = require('util');
const client = redis.createClient();
client.get = utils.promisify(client.get).bind(client);
client.set = utils.promisify(client.set).bind(client);

// create Kue
const kue = require('kue');
const queue = kue.createQueue();
let reservationEnabled = true;

// App Server
const express = require('express');
// Create an express server listening on the port 1245.
const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`Listening on port ${port}: http://localhost:${port}`);
});

// Create a function reserveSeat, that will take into argument number,
// and set the key available_seats with the number
function reserveSeat(num) {
  client.set('available_seats', `${num}`);
}

// Create a function getCurrentAvailableSeats,
// it will return the current number of available seats (by using promisify for Redis)
async function getCurrentAvailableSeats() {
  const seatData = await client.get('available_seats');
  return seatData;
}
// When launching the application, set the number of available to 50
// Initialize the boolean reservationEnabled to true - it will be turn to false when no seat will be available
client.on('connect', () => {
  console.log('Redis client connected to the server');
  reserveSeat(50);
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// get the availble seats
app.get('/available_seats', async (req, res) => {
  const data = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: data });
});

// get reserved seats
app.get('/reserve_seat', async (req, res) => {
  if (reservationEnabled === false) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat');
  job.save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
      return;
    }
    res.json({ status: 'Reservation in process' });
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job JOB_ID failed: ${err}`);
  });
});

// process reservation
app.get('/process', (req, res) => {
  // Process the queue
  queue.process('reserve_seat', async (job, done) => {
    // Retrieve available seats count before processing the queue
    let availableSeats = parseInt(await getCurrentAvailableSeats());
    if (availableSeats === 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      availableSeats -= 1;
      reserveSeat(availableSeats);
      done();
    }
  });
  res.json({ status: 'Queue processing' });
});
