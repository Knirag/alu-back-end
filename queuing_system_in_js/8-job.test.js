const kue = require("kue");
const { expect } = require("chai"); 

const createPushNotificationsJobs = require("./8-job");

describe("createPushNotificationsJobs function", () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter(); // Enter test mode
  });

  afterEach(() => {
    queue.testMode.exit(); // Exit test mode
    queue.clear(); // Clear the queue
  });

  it("throws an error if jobs is not an array", () => {
    const invalidJobs = "not an array";
    expect(() => createPushNotificationsJobs(invalidJobs, queue)).to.throw(
      "Jobs is not an array"
    );
  });

  it("creates jobs in the queue for each job in the list", () => {
    const jobs = [
      { phoneNumber: "1234567890", message: "Test message 1" },
      { phoneNumber: "9876543210", message: "Test message 2" },
    ];

    createPushNotificationsJobs(jobs, queue);

    const queuedJobs = queue.testMode.inactive();
    expect(queuedJobs.length).to.equal(jobs.length);
    queuedJobs.forEach((job, index) => {
      expect(job.type).to.equal("push_notification_code_3");
      expect(job.data).to.deep.equal(jobs[index]);
    });
  });
});
