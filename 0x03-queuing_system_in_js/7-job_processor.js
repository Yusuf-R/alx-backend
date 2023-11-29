/* eslint-disable import/newline-after-import */
/* eslint-disable no-console */
const blacklist = ['4153518780', '4153518781'];

function sendNotification(phoneNumber, message, job, done) {
  // Track the progress of the job of 0 out of 100
  job.progress(0, 100);
  // Convert phoneNumber to string
  const phoneNumberString = phoneNumber.toString();
  if (blacklist.includes(phoneNumberString)) {
    // If phoneNumber is blacklisted, fail the job
    done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    // Track the progress to 50%
    job.progress(50, 100);
    // Log to the console Sending notification to PHONE_NUMBER, with message: MESSAGE
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    // Pass the job to done after processing
    done();
  }
}
const kue = require('kue');
const queue = kue.createQueue();

// Process the queue push_notification_code_2 with two jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
