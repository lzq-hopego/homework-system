// 环境配置文件

// 环境分为三种
//     1、开发环境
//     2、线上环境
//     3、测试环境

// 获取当前环境
const env=import.meta.env.MODE || 'prod'

const EnvConfig={
    development:{
        baseApi:'//127.0.0.1/api',
        mockApi:'https://domain.com/api',
    },
    test:{
        baseApi:'://domain.com/api',
        mockApi:'https://domain.com/api',
    },
    production:{
        baseApi:'//domain.com/api',
        mockApi:'https://domain.com/api',
    },
}

export default{
    env,
    mock:true,//mock总开关
    ...EnvConfig[env]
}