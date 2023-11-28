/* eslint-disable no-console */
import { createClient } from 'redis';

const util = require('util');

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Manually promisify the nedded functions in the client object
client.getAsync = util.promisify(client.get).bind(client);
client.setAsync = util.promisify(client.set).bind(client);

async function setNewSchool(schoolName, value) {
  try {
    const reply = await client.setAsync(schoolName, value);
    console.log(`Reply: ${reply}`);
  } catch (err) {
    console.error(err);
  }
}

async function displaySchoolValue(schoolName) {
  try {
    const reply = await client.getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.error(err);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
