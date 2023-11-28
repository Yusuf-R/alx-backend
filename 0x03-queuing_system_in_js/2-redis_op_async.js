/* eslint-disable no-console */
const util = require('util');
const { createClient } = require('redis');

const client = createClient();

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
