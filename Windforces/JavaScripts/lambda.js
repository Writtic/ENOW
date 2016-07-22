var http = require('http');

var options = {
  host : 'https://hooks.slack.com',
  port : 80,
  path : '/services/T1P5CV091/B1PV8CWHX/eIrXpSWVLng44bdMJkEOQltr',
  method : 'POST',
};

exports.handler = function(event, context) {
  array = event['array'];
  array.forEach(function(element) {
    var dictionary = ' { ' +
    ' "username" : ' +
    '"' + element['id'] + '"' + ' , ' +
    ' "text" : ' +
    '"' + element['selftext'] + '"' + ' , ' +
    ' "channel" : "#webhook_test"' +
    ' } ';
    console.log(dictionary);

  });
  var json = JSON.parse(dictionary);

  var request = http.request(optios, function(resource) {
    console.log("Status : " + resource.statusCode);
    resource.setEncoding("utf8")
    resource.on("data", function(body){
      console.log("Body : " + body);
    });
  });
  request.on("error", function(error) {
    console.log("problem with request : " + error.message);
  });

  request.write(json);
  request.end();
};
