const fs = require("fs");

function countStudents(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, "utf8", processData); 

    function processData(err, data) {
      // Separate function for processing data
      if (err) {
        reject(Error("Cannot load the database"));
        return;
      }

      const response = [];
      processDataHelper(data, response, resolve); 
    }

    function processDataHelper(data, response, resolve) {
      const content = data.toString().split("\n");
      const students = content.filter((item) => item.trim());

      const studentCount = students.length > 1 ? students.length - 1 : 0;
      const message = `Number of students: ${studentCount}`;
      console.log(message);
      response.push(message);

      const fields = {};
      for (const i in students) {
        if (i !== "0") {
          
          if (!fields[students[i][3]]) fields[students[i][3]] = [];
          fields[students[i][3]].push(students[i][0]);
        }
      }

      delete fields["field"];

      for (const key of Object.keys(fields)) {
        const message = `Number of students in ${key}: ${
          fields[key].length
        }. List: ${fields[key].join(", ")}`;
        console.log(message);
        response.push(message);
      }

      resolve(response); 
    }
  });
}

module.exports = countStudents;
