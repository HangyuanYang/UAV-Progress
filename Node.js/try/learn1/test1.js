'use strict';

var fs = require('fs');

try {
    var data = fs.readFileSync('sample.txt', 'utf-8');
    console.log(data);
} catch (err) {
    // 出错了
}


fs.readFile('sample.txt', 'utf-8', function (err, data) {
    if (err) {
        console.log(err);
    } else {
        //console.log(data);
    }
});

fs.readFile('sample.jpg', function (err, data) {
    if (err) {
        console.log(err);
    } else {
        var text;
        var buf;

    //当读取二进制文件时，不传入文件编码时，回调函数的data参数将返回一个Buffer对象。在Node.js中，
    //Buffer对象就是一个包含零个或任意个字节的数组（注意和Array不同）。Buffer对象可以和String作转换
        //console.log(data);
        text = data.toString('utf-8');
        buf = Buffer.from(text, 'utf-8');
        //console.log("110");
        console.log(buf);//没输出?
    }
});