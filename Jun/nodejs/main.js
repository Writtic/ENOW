// test
var http = require('http');

var server = http.createServer(helloResponse);

function helloResponse(req, res) {
    res.writeHead(200, {
        'Content-Type': 'text/plain'
    });
    res.end('Hello World\n');
}
server.listen(8000);
