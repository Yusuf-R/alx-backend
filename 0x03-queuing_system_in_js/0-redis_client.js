/* eslint-disable no-console */
import { createClient } from 'redis';

function redisServer() {
  const client = createClient();

  client.on('connect', () => {
    console.log('Redis client connected to the server');
  });

  client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
  });
}

module.exports = redisServer;
