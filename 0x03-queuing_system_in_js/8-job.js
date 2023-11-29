/* eslint-disable no-console */
// create a function named createPushNotificationsJobs:

// It takes into argument jobs (array of objects), and queue (Kue queue)
// If jobs is not an array, it should throw an Error with message: Jobs is not an array
// For each job in jobs, create a job in the queue push_notification_code_3
// When a job is created, it should log to the console Notification job created: JOB_ID
// When a job is complete, it should log to the console Notification job JOB_ID completed
// When a job is failed, it should log to the console Notification job JOB_ID failed: ERROR
// When a job is making progress,
// it should log to the console Notification job JOB_ID PERCENT% complete

function createPushNotificationsJobs(jobs, queue) {
  // test if jobs is an array
  if (!Array.isArray(jobs)) {
    throw Error('Jobs is not an array');
  }
  // for each jobs create a job in the queue push_notification_code_3
  jobs.forEach((jobData) => {
    const job = queue.create('push_notification_code_3', jobData);
    job.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${job.id}`);
      }
    });
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
}

module.exports = createPushNotificationsJobs;
