var buf = new Buffer("Simply Easy Learning");
var json = buf.toJSON(buf);

console.log(json);

var dictionary = '{' +
' "id" : "identification", ' +
' "password" : "credentials" ' +
'}';

json = JSON.parse(dictionary)

console.log(json);
console.log(json['id']);
