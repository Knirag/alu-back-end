export default function appendToEachArrayValue(array, appendString) {
  for (const value of array) {
    // Use 'const' for loop iteration
    const index = array.indexOf(value); // Find index of current value
    array[index] = appendString + value; // Modify element at the index
  }

  return array;
}
