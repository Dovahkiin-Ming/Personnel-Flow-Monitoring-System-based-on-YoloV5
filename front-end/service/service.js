const express = require('express');
const app = express();
const path = require('path');

app.use(express.static(path.join(__dirname,'../dist')));

app.listen(8889, '127.0.0.1')
console.log('前端服务器开启成功====>>>http://127.0.0.1:8889/');
console.log('前端服务器开启成功====>>>http://127.0.0.1:8889/');
console.log('前端服务器开启成功====>>>http://127.0.0.1:8889/');
console.log('重要的事情说三遍');
console.log('最后编译时间2023年5月9日21点37分');