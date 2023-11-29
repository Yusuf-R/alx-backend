/* eslint-disable no-unused-expressions */
/* eslint-disable object-curly-newline */
const sinon = require('sinon');
const { expect } = require('chai');
const kue = require('kue');
const { beforeEach, afterEach, it, describe } = require('mocha');
const { createPushNotificationsJobs } = require('./8-job');

describe('createPushNotificationsJobs', () => {
  let queue;
  let testJobs;

  beforeEach(() => {
    // Arrange
    queue = kue.createQueue();
    testJobs = [
      { phoneNumber: '1234567890', message: 'Message 1' },
      { phoneNumber: '0987654321', message: 'Message 2' },
    ];
  });

  afterEach(() => {
    // Clean up
    queue.shutdown();
  });

  it('should create jobs for each item in the jobs array', (done) => {
    // Arrange
    const createSpy = sinon.spy(queue, 'create');

    // Act
    createPushNotificationsJobs(testJobs, queue);

    // Assert
    setTimeout(() => {
      expect(createSpy.callCount).to.equal(testJobs.length);
      testJobs.forEach((jobData, index) => {
        expect(createSpy.getCall(index).args[0]).to.equal('push_notification_code_3');
        expect(createSpy.getCall(index).args[1]).to.equal(jobData);
      });
      done();
    }, 10); // Adjust the delay as needed
  });

  it('should throw an error if jobs is not an array', () => {
    // Arrange
    const badJobs = { phoneNumber: '1234567890', message: 'Not an array' };

    // Act & Assert
    expect(() => createPushNotificationsJobs(badJobs, queue)).to.throw('Jobs is not an array');
  });

  it('should log job creation', (done) => {
    // Arrange
    const consoleLogSpy = sinon.spy(console, 'log');

    // Act
    createPushNotificationsJobs(testJobs, queue);

    // Assert
    setTimeout(() => {
      expect(consoleLogSpy.calledWithMatch(/Notification job created:/)).to.be.true;
      consoleLogSpy.restore();
      done();
    }, 10); // Adjust the delay as needed
  });

  it('should log job completion', (done) => {
    // Arrange
    const job = queue.create('push_notification_code_3', testJobs[0]).save(() => {});
    const completeSpy = sinon.spy();
    job.on('complete', completeSpy);

    // Act
    job.emit('complete');

    // Assert
    setTimeout(() => {
      expect(completeSpy.called).to.be.true;
      done();
    }, 10); // Adjust the delay as needed
  });

  it('should log job failure', (done) => {
    // Arrange
    const job = queue.create('push_notification_code_3', testJobs[0]).save(() => {});
    const failedSpy = sinon.spy();
    job.on('failed', failedSpy);

    // Act
    job.emit('failed', new Error('Failed'));

    // Assert
    setTimeout(() => {
      expect(failedSpy.called).to.be.true;
      done();
    }, 10); // Adjust the delay as needed
  });

  it('should log job progress', (done) => {
    // Arrange
    const job = queue.create('push_notification_code_3', testJobs[0]).save(() => {});
    const progressSpy = sinon.spy();
    job.on('progress', progressSpy);

    // Act
    job.emit('progress', 50);

    // Assert
    setTimeout(() => {
      expect(progressSpy.calledWith(50)).to.be.true;
      done();
    }, 10); // Adjust the delay as needed
  });
});
