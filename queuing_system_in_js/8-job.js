const kue = require("kue"); // Import Kue library

function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error("Jobs is not an array");
  }

  // Loop through each job in the array
  jobs.forEach((job) => {
    const pushNotificationJob = queue
      .createJob("push_notification_code_3", job)
      .on("complete", (result) => {
        console.log(`Notification job ${result.id} completed`);
      })
      .on("failed", (err, errJob) => {
        console.error(`Notification job ${errJob.id} failed: ${err.message}`);
      })
      .on("progress", (progress) => {
        console.log(
          `Notification job ${progress.jobId} ${progress.percent}% complete`
        );
      });

    console.log(`Notification job created: ${pushNotificationJob.id}`);
  });
}

module.exports = createPushNotificationsJobs;
