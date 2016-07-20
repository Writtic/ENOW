var events = require('events');
var EventEmitter = new events.EventEmitter();

var listener1 = function listener1(){
  console.log("listener1 executed");
}

var listener2 = function listener2(){
  console.log("listener2 executed");
}

EventEmitter.addListener("connection", listener1);
EventEmitter.on("connection", listener2);

var eventListeners = require('events').EventEmitter.listenerCount(EventEmitter, "connection");
console.log(eventListeners + " Listener(s) listening to connection event");

EventEmitter.emit("connection");

EventEmitter.removeListener("connection", listener1)
console.log("Listener 1 will not listen now.");

EventEmitter.emit("connection");

eventListeners = require("events").EventEmitter.listenerCount(EventEmitter, "connection");
console.log(eventListeners + " Listener(s) listening to connection event");

console.log("Program Ended");
