/* eslint-disable no-console */

import redis from 'redis';

const publisher = redis.createClient();

publisher.on('connect', () => {
  console.log('Redis client connected to the server');
});

publisher.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish('holberton school channel', message);
  }, time);
}

// Example usage:
publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);
publishMessage('Hello, world!', 2000); // Publish 'Hello, world!' after 2000 milliseconds
publishMessage('KILL_SERVER', 4000); // Publish 'KILL_SERVER' after 4000 milliseconds
