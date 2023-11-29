/* eslint-disable no-console */
import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// subscribe to the channel holberton school channel
// When it receives message on the channel holberton school channel,
// it should log the message to the console
// When the message is KILL_SERVER, it should unsubscribe and quit

/* this way much easier that setting up another instance of redis */
const subscriber = client.duplicate();

subscriber.subscribe('holberton school channel');

subscriber.on('message', (channel, message) => {
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
  if (channel === 'holberton school channel') {
    console.log(message);
  }
});

// Handle unsubscribing and quitting on process exit
process.on('SIGINT', () => {
  subscriber.unsubscribe();
  subscriber.quit();
});
