## 配置

```
vim ./src/config/index.js
```



```
 11 const EnvConfig={
 12     development:{
 13         baseApi:'//127.0.0.1/api',//开发环境
 14         mockApi:'https://domain.com/api', 
 15     },
 16     test:{
 17         baseApi:'://domain.com/api',//测试环境
 18         mockApi:'https://domain.com/api',
 19     },
 20     production:{
 21         baseApi:'//domain.com/api',//线上环境
 22         mockApi:'https://domain.com/api',
 23     },
 24 }
```



## 使用

- 安装依赖

  ```
  yarn install
  ```

- 本地测试

  ```
  yarn dev
  ```

- 发行

  ```
  yarn build
  ```

  
