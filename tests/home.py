var request = require('request');
var options = {
  'method': 'GET',
  'url': 'http://localhost:4000/',
  'headers': {
  }
};
request(options, function (error, response) {
  if (error) throw new Error(error);
  console.log(response.body);
});
