'use strict';

var fs = require('fs');

var data ={"name":"shenyanhao","attribute":"dalao"};
var data_json=JSON.stringify(data,null,' ');
fs.writeFile('output.txt', data_json, function (err) {
    if (err) {
        console.log(err);
    } else {
        console.log('ok.');
    }
});
fs.writeFileSync('output.txt', data);