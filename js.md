###[廖雪峰的官方网站-Javascript教程](https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000)

- [x] 快速入门

      - [x] 基本语法

      - [x] 数据类型和变量

            Infinity NaN  isNaN(NaN);判断NaN

            Math.abs(1 / 3 - (1 - 2 / 3)) < 0.0000001 判断浮点数相等

            null和undefined  strict模式

      - [x] 字符串

            `\u####`表示一个Unicode字符  *`* ...*`* 多行字符串  把多个字符串连接起来，可以用`+`号连接

            模板字符串 toUpperCase toLowerCase indexOf  substring

      - [x] 数组

            取得`Array`的长度，直接访问`length`属性 直接给`Array`的`length`赋一个新值会导致`Array`大小的变化

            索引赋值时，索引超过了范围，同样会引起`Array`大小的变化

            indexOf slice push和pop  unshift和shift sort reverse splice concat join split

      - [x] 对象

            in  hasOwnProperty

      - [x] 条件判断

      - [x] 循环

            for ... in

            过滤掉对象继承的属性，用`hasOwnProperty()`来实现

            `for ... in`循环可以直接循环出`Array`的索引；

      - [x] Map和Set

      - [x] iterable

            `Array`、`Map`和`Set`都属于`iterable`类型

            具有`iterable`类型的集合可以通过新的`for ... of`循环来遍历

            更好的方式是直接使用`iterable`内置的`forEach`方法

            ```javascript
            a.forEach(function (element, index, array) {
              // element: 指向当前元素的值
              // index: 指向当前索引
              // array: 指向Array对象本身
            };
            ```

- [x] 函数

      - [x] 函数定义和调用

            JavaScript的函数也是一个对象，abs()函数实际上是一个函数对象，函数名`abs`可视为指向该函数的变量

            没有`return`语句，函数执行完毕后也会返回结果，只是结果为`undefined`

            参数检查typeof x !== 'number' **arguments**  利用`arguments`，你可以获得调用者传入的所有参数

            ```javascript
            function foo(a, b, ...rest) {
            }//为了获得额外的rest参数
            ```

            return r * r * (pi || 3.14);  在一个操作数**不是**布尔值的情况下，不一定返回布尔值，会遵循一些规则

      - [x] 变量作用域与解构赋值

            内部函数可以访问外部函数定义的变量，反过来则不行

            JavaScript的函数在查找变量时从自身函数定义开始，从“内”向“外”查找。如果内部函数定义了与外部函数重名的变量，则内部函数的变量将“屏蔽”外部函数的变量

            **变量提升**   在函数内部首先申明所有变量

            ```
            function foo() {
                var
                    x = 1, // x初始化为1
                    y = x + 1, // y初始化为2
                    z, i; // z和i为undefined
                // 其他语句:
            }
            ```

            JavaScript默认有一个全局对象`window`，全局作用域的变量实际上被绑定到`window`的一个属性

            名字空间   自己的所有变量和函数全部绑定到一个全局变量中减少冲突

            块级作用域的变量 `let`，用`let`替代`var`可以申明一个块级作用域的变量   const

            **解构赋值**

            * 对数组元素进行解构赋值时，多个变量要用`[...]`括起来

            * 一个对象中取出若干属性，也可以使用解构赋值

              要使用的变量名和属性名不一致，可以用下面的语法获取 let {name, passport:id} = person;

            ​       构赋值还可以使用默认值，避免了属性返回`undefined`的问题 var {name, single=true} = person;

            `{`开头的语句当作了块处理 解决方法是用小括号括起来      ({x, y} = { name: '小明', x: 100, y: 200});

            使用场景  交换;快速获取当前页面的域名和路径;函数接收一个对象作为参数,那么,可以使用解构直接把对象的属性绑定到变量中

      - [x] 方法

            一个对象中绑定函数   **要保证`this`指向正确，必须用`obj.xxx()`的形式调用**

            `this`指针只在`age`方法的函数内指向`xiaoming`，在函数内部定义的函数，`this`又指向`undefined`了！（在非strict模式下，它重新指向全局对象`window`！）

            修复的办法也不是没有，我们用一个`that`变量首先捕获`this`

            ```
            age: function () {
                    var that = this; // 在方法内部一开始就捕获this
                    function getAgeFromBirth() {
                        var y = new Date().getFullYear();
                        return y - that.birth; // 用that而不是this
                    }
                    return getAgeFromBirth();
                }
            ```

            另一个与`apply()`类似的方法是`call()`，唯一区别是：

            - `apply()`把参数打包成`Array`再传入；
            - `call()`把参数按顺序传入。

      - [x] 高阶函数

            - [x] map/reduce

                   字符串转为数字：

                  x.charCodeAt() - 48

                  ```javascript
                  // Consider:
                  ['1', '2', '3'].map(parseInt);
                  // While one could expect [1, 2, 3]
                  // The actual result is [1, NaN, NaN]
                
                  // parseInt is often used with one argument, but takes two.
                  // The first is an expression and the second is the radix.
                  // To the callback function, Array.prototype.map passes 3 arguments: 
                  // the element, the index, the array
                  // The third argument is ignored by parseInt, but not the second one,
                  // hence the possible confusion. See the blog post for more details
                
                  function returnInt(element) {
                    return parseInt(element, 10);
                  }
                
                  ['1', '2', '3'].map(returnInt); // [1, 2, 3]
                  // Actual result is an array of numbers (as expected)
                
                  // Same as above, but using the concise arrow function syntax
                  ['1', '2', '3'].map( str => parseInt(str) );
                
                  // A simpler way to achieve the above, while avoiding the "gotcha":
                  ['1', '2', '3'].map(Number); // [1, 2, 3]
                  // but unlike `parseInt` will also return a float or (resolved) exponential notation:
                  ['1.1', '2.2e2', '3e300'].map(Number); // [1.1, 220, 3e+300]
                  ```
                
                  ​

            - [x] filter

            - [x] sort

                  `Array`的`sort()`方法默认把所有元素先转换为String再排序

                  `sort()`方法也是一个高阶函数，它还可以接收一个比较函数来实现自定义的排序

                  ```javascript
                  arr.sort(function (x, y) {
                  	if (x < y) {
                      	return -1;
                  	}
                  	if (x > y) {
                      	return 1;
                  	}
                  	return 0;
                  });
                  ```
                  `sort()`方法会直接对`Array`进行修改，它返回的结果仍是当前`Array`

            ******

            2017.11.11-2017.11.24

      - [x] 闭包

        高阶函数可以将函数作为返回值

        `lazy_sum()`时，返回的并不是求和结果，而是求和函数->调用函数`f`时，才真正计算求和的结果

        当`lazy_sum`返回函数`sum`时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”程序结构

        返回闭包时牢记的一点就是：**返回函数不要引用任何循环变量，或者后续会发生变化的变量**

        一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变

        ```javascript
        function count() {
            var arr = [];
            for (var i=1; i<=3; i++) {
                arr.push((function (n) {
                    return function () {
                        return n * n;
                    }
                })(i));
            }
            return arr;
        }

        var results = count();
        var f1 = results[0];
        var f2 = results[1];
        var f3 = results[2];
        ```

        ​

        借助闭包，同样可以封装一个私有变量->闭包就是携带状态的函数，并且它的状态可以完全对外隐藏起来

      - [x] 箭头函数

            lambda表达式 x => x * x       (x, y) => x * x + y * y         () => 3.14

            ```javascript
            (x, y, ...rest) => {
                var i, sum = x + y;
                for (i=0; i<rest.length; i++) {
                    sum += rest[i];
                }
                return sum;
            }
            ```

            返回对象`x => ({ foo: x })`  不能：`x => { foo: x }`会有语法冲突

            ```javascript
            arr.sort((x, y) => {
                if (x<y)return -1;
                return 1;
            });//-1不用交换 1交换
            ```

      - [x] generator

            `for ... of`循环迭代generator对象，这种方式不需要我们自己判断`done`

            因为generator可以在执行过程中多次返回，所以它看上去就像一个可以记住执行状态的函数，利用这一点，写一个generator就可以实现需要用面向对象才能实现的功能

            generator还有另一个巨大的好处，就是把异步回调代码变成“同步”代码

- [x] 标准对象

      **包装对象**

      - [x] Date

             JavaScript的Date对象月份值从0开始，牢记0=1月，1=2月，2=3月，……，11=12月。

            使用Date.parse()时传入的字符串使用实际月份01~12，转换为Date对象后getMonth()获取的月份值为0~11。

      - [x] [***RegExp***](https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000/001434499503920bb7b42ff6627420da2ceae4babf6c4f2000)

            基本语法,进阶,切分字符串

            test()测试给定的字符串是否符合条件

            分组

            `exec()`方法在匹配成功后，会返回一个`Array`，第一个元素是正则表达式匹配到的整个字符串，后面的字符串表示匹配成功的子串。

            贪婪匹配  加个`?`就可以让`\d+`采用非贪婪匹。

            全局搜索  全局匹配可以多次执行`exec()`方法来搜索一个匹配的字符串,当我们指定`g`标志后，每次运行`exec()`，正则表达式本身会更新`lastIndex`属性，表示上次匹配到的最后索引。

            var re = /^[\w.]+?\@\w+?\.\w+$/;  			匹配邮箱1

            var re = /^<([\w\s]*)>\s*([\w.]+?\@\w+?.\w+)$/;  	匹配邮箱2

      - [x] JSON

            把任何JavaScript对象变成JSON，就是把这个对象序列化成一个JSON格式的字符串，这样才能够通过网络传递给其他计算机。

            如果我们收到一个JSON格式的字符串，只需要把它反序列化成一个JavaScript对象，就可以在JavaScript中直接使用这个对象了。   

            var s = JSON.stringify(xiaoming); 

            要输出得好看一些，可以加上参数，按缩进输出 JSON.stringify(xiaoming, null, '  ');

            第二个参数用于控制如何筛选对象的键值 JSON.stringify(xiaoming, ['name', 'skills'], '  ');

            还可以传入一个函数，这样对象的每个键值对都会被函数先处理

            ```javascript
            function convert(key, value) {
                    if (typeof value === 'string') {
                    	return value.toUpperCase();
                    }
                    return value;
            }
            JSON.stringify(xiaoming, convert, '  ');
            ```

            精确控制如何序列化小明，可以给`xiaoming`定义一个`toJSON()`的方法，直接返回JSON应该序列化的数据。

            **反序列化** JSON.parse()

            `JSON.parse()`还可以接收一个函数，用来转换解析出的属性                                                                                                     



- [x] 面向对象编程

      * [x] 创建对象

      JavaScript还可以用一种构造函数的方法来创建对象。它的用法是，先定义一个构造函数：

      ```javascript
      function Student(name) {
          this.name = name;
          this.hello = function () {
              alert('Hello, ' + this.name + '!');
          }
      }
      ```

      用关键字`new`来调用这个函数，并返回一个对象。

      可以编写一个`createStudent()`函数，在内部封装所有的`new`操作:

      ```javascript
      function Student(props) {
          this.name = props.name || '匿名'; // 默认值为'匿名'
          this.grade = props.grade || 1; // 默认值为1
      }

      Student.prototype.hello = function () {
          alert('Hello, ' + this.name + '!');
      };

      function createStudent(props) {
          return new Student(props || {})
      }
      ```

      * [x] 原型继承

      把继承这个动作用一个`inherits()`函数封装起来，还可以隐藏`F`的定义:

      ```javascript
      function inherits(Child, Parent) {
          var F = function () {};
          F.prototype = Parent.prototype;
          Child.prototype = new F();
          Child.prototype.constructor = Child;
      }
      ```

      这个`inherits()`函数可以复用：

      ```javascript
      function Student(props) {
          this.name = props.name || 'Unnamed';
      }

      Student.prototype.hello = function () {
          alert('Hello, ' + this.name + '!');
      }

      function PrimaryStudent(props) {
          Student.call(this, props);
          this.grade = props.grade || 1;
      }

      // 实现原型继承链:
      inherits(PrimaryStudent, Student);

      // 绑定其他方法到PrimaryStudent原型:
      PrimaryStudent.prototype.getGrade = function () {
          return this.grade;
      };
      ```

      JavaScript的原型继承实现方式就是：

      1. 定义新的构造函数，并在内部用`call()`调用希望“继承”的构造函数，并绑定`this`；
      2. 借助中间函数`F`实现原型链继承，最好通过封装的`inherits`函数完成；
      3. 继续在新的构造函数的原型上定义新方法。

      * [x] class继承

      ```javascript
      class PrimaryStudent extends Student {
          constructor(name, grade) {
              super(name); // 记得用super调用父类的构造方法!
              this.grade = grade;
          }

          myGrade() {
              alert('I am at grade ' + this.grade);
          }
      }
      ```


- [ ] 浏览器
- [ ] jQuery
- [ ] 错误处理
- [ ] underscore
- [x] Node.js
      * [x] 安装Node.js和npm，搭建环境，模块
      * [x] 基本模块
            * [x] fs   文件
            * [x] stream  流操作
            * [x] http    http服务器程序
            * [ ] crypto   加密



- [ ] React

