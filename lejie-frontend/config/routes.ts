export default [
    {
        path: '/user',
        layout: false,
        routes: [
            { name: '登录', path: '/user/login', component: './User/Login' },
            { name: '注册账号', path: '/user/register', component: './User/Register' },
            { name: '注册账号', path: '/user/register/:id', component: './User/Register', hideInMenu: true},
        ],
    },
    { path: '/welcome', name: '主页', icon: 'smile', component: './Index/index' },
    { path: '/interfaceInfo/:id', name: '查看接口', icon: 'smile', component: './InterfaceInfo/index', hideInMenu: true},
    {
        path: '/admin',
        name: '管理页',
        icon: 'crown',
        access: 'canAdmin',
        routes: [
            { name: '接口管理', icon: 'table', path: '/admin/interfaceInfo', component: './Admin/InterfaceInfo' },
            { name: '接口分析', icon: 'table', path: '/admin/analysis', component: './Admin/analysis' },
        ],
    },
    { path: '/account/center', name: '个人中心', icon: 'UserOutlined', component: './User/Info', hideInMenu: false},
    { path: '/', redirect: '/welcome' },
    { path: '*', layout: false, component: './404' },
];
