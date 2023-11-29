/* eslint-disable no-console */

// Create a queue with Kue
// Create a queue named push_notification_code, and create a job with the object created before
// When the job is created without error, log to the console Notification job created: JOB ID
// When the job is completed, log to the console Notification job completed
// When the job is failing, log to the console Notification job failed
const kue = require('kue');

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '1234567890',
  message: 'Hello, world!',
};
// create job
const job = queue.create('push_notification_code', jobData);

// save and log job
job.save((err) => {
  if (!err) {
    console.log(`Notification job created: ${job.id}`);
  }
});

// process the job when completed
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (err) => {
  console.log(`Notification job failed: ${err}`);
});
