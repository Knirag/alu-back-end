export default function createEmployeesObject(departmentName, employees) {
  return {
    [`$${departmentName}`]: employees, // Use template literal for dynamic property name
  };
}

export default function createReportObject(employeesList) {
  const allEmployees = {};

  // Iterate over each department in employeesList
  for (const department in employeesList) {
    allEmployees[department.slice(2)] = employeesList[department]; // Remove leading "$$"
  }

  return {
    allEmployees,
    getNumberOfDepartments() { // Method property using arrow function
      return Object.keys(employeesList).length;
    },
  };
}
