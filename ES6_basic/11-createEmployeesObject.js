export default function createEmployeesObject(departmentName, employees) {
  return {
    [`$${departmentName}`]: employees, // Use template literal for dynamic property name
  };
}
