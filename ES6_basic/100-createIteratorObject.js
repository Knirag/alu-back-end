export default function createIteratorObject(report) {
  const allDepartments = Object.entries(report.allEmployees); // Get department entries
  let currentDepartmentIndex = 0;
  let currentEmployeeIndex = 0;

  return {
    next() {
      if (currentDepartmentIndex >= allDepartments.length) {
        return { done: true };
      }

      const [departmentName, employees] =
        allDepartments[currentDepartmentIndex];

      if (currentEmployeeIndex >= employees.length) {
        currentDepartmentIndex++;
        currentEmployeeIndex = 0;
        return this.next(); // Recursively call next if department ends
      }

      const employee = employees[currentEmployeeIndex];
      currentEmployeeIndex++;

      return { value: { department: departmentName, employee }, done: false };
    },
  };
}
