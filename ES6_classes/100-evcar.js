import Car from "./10-car.js";

class EVCar extends Car {
  constructor(brand, motor, color, range) {
    super(brand, motor, color); // Call the parent constructor
    this._range = range; // Store range as a private property
  }

  get range() {
    return this._range;
  }

  set range(value) {
    this._range = value;
  }

  cloneCar() {
    return new Car(this.brand, this.motor, this.color);
  }
}

export default EVCar;
