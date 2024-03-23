export default function iterateThroughObject(reportWithIterator) {
  let employeeNames = ""; // Initialize an empty string to store employee names
  let currentEmployee;

  while (!(currentEmployee = reportWithIterator.next()).done) {
    employeeNames += `${currentEmployee.value.employee} | `; // Add employee name with separator
  }

  // Remove the trailing separator for a cleaner output
  return employeeNames.slice(0, -2);
}
