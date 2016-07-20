var events = require('events');

var evenEmitter = new events.EventEmitter();

var connectHandler = function connected() {
  console.log("connection successful");
  evenEmitter.emit("data_received");
}

evenEmitter.on("connection", connectHandler);
evenEmitter.on("data_received", function() {
  console.log("data received successfully.");
});

evenEmitter.emit("connection");
console.log("Program Ended");
