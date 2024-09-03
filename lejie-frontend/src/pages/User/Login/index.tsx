import { Footer } from '@/components';
import {
    AlipayCircleOutlined,
    LockOutlined,
    MobileOutlined,
    TaobaoCircleOutlined,
    UserOutlined,
    WeiboCircleOutlined,
} from '@ant-design/icons';
import {
    LoginForm,
    ProFormCaptcha,
    ProFormCheckbox,
    ProFormText,
} from '@ant-design/pro-components';
import { Helmet, history, Link, useModel } from '@umijs/max';
import { Alert, message, Tabs } from 'antd';
import { createStyles } from 'antd-style';
import React, { useState } from 'react';
import Settings from '../../../../config/defaultSettings';
import { getCaptchaUsingGET, userCurrentGet, userEmailLoginUsingPOST, userTokenPost } from '@/services/lejie-backend/user';

const useStyles = createStyles(({ token }) => {
    return {
        action: {
            marginLeft: '8px',
            color: 'rgba(0, 0, 0, 0.2)',
            fontSize: '24px',
            verticalAlign: 'middle',
            cursor: 'pointer',
            transition: 'color 0.3s',
            '&:hover': {
                color: token.colorPrimaryActive,
            },
        },
        lang: {
            width: 42,
            height: 42,
            lineHeight: '42px',
            position: 'fixed',
            right: 16,
            borderRadius: token.borderRadius,
            ':hover': {
                backgroundColor: token.colorBgTextHover,
            },
        },
        container: {
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            overflow: 'auto',
            backgroundImage:
                "url('https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/V-_oS6r-i7wAAAAAAAAAAAAAFl94AQBr')",
            backgroundSize: '100% 100%',
        },
    };
});
const ActionIcons = () => {
    const { styles } = useStyles();
    return (
        <>
            <AlipayCircleOutlined key="AlipayCircleOutlined" className={styles.action} />
            <TaobaoCircleOutlined key="TaobaoCircleOutlined" className={styles.action} />
            <WeiboCircleOutlined key="WeiboCircleOutlined" className={styles.action} />
        </>
    );
};

const LoginMessage: React.FC<{
    content: string;
}> = ({ content }) => {
    return (
        <Alert
            style={{
                marginBottom: 24,
            }}
            message={content}
            type="error"
            showIcon
        />
    );
};
const Login: React.FC = () => {
    const [userLoginState, setUserLoginState] = useState<API.LoginResult>({});
    const [type, setType] = useState<string>('account');
    const { initialState, setInitialState } = useModel('@@initialState');
    const { styles } = useStyles();

    const doLoading = async () => {
        const res = await userCurrentGet()
        if (res.ret === 0 && res.data) {
            message.success('登录成功！');
            const urlParams = new URL(window.location.href).searchParams;
            history.push(urlParams.get('redirect') || '/');
            setInitialState({
                loginUser: res.data,
                settings: initialState?.settings
            });
            return;
        } else {
            message.error(res.msg)
            return
        }
    }

    const handleSubmit = async (values: API.UserLogin) => {
        try {
            // 登录
            if (!localStorage.getItem('access_token')) {
                const tokenRes = await userTokenPost({
                    username: values.userAccount,
                    password: values.userPassword
                })
                localStorage.setItem('access_token', tokenRes.access_token)
            }
            await doLoading()
        } catch (error) {
            const defaultLoginFailureMessage = '登录失败，请重试！';
            message.error(defaultLoginFailureMessage);
        }
    };

    const handleEmailSubmit = async (values: UserAPI.EmailLoginRequest) => {
        try {
            // 登录
            if (!localStorage.getItem('access_token')) {
                const tokenRes = await userEmailLoginUsingPOST({
                    ...values
                })
                if (tokenRes.ret === 0 && tokenRes.data) {
                    localStorage.setItem('access_token', tokenRes.data.access_token)
                } else {
                    message.error(tokenRes.msg)
                    return
                }
            }
            await doLoading()
        } catch (error) {
            const defaultLoginFailureMessage = '登录失败，请重试！';
            message.error(defaultLoginFailureMessage);
        }
    }

    const { status, type: loginType } = userLoginState;
    return (
        <div className={styles.container}>
            <Helmet>
                <title>
                    {'登录'}- {Settings.title}
                </title>
            </Helmet>
            <div
                style={{
                    flex: '1',
                    padding: '32px 0',
                }}
            >
                <LoginForm
                    contentStyle={{
                        minWidth: 280,
                        maxWidth: '75vw',
                    }}
                    logo={<img alt="logo" src="/logo.svg" />}
                    title={Settings.title}
                    subTitle={'致力于提供稳定、安全、高效的接口调用服务'}
                    initialValues={{
                        autoLogin: true,
                    }}
                    actions={['其他登录方式 :', <ActionIcons key="icons" />]}
                    onFinish={async (values) => {
                        if (type === 'account') {
                            await handleSubmit(values as API.UserLogin);
                        } else {
                            await handleEmailSubmit(values as UserAPI.EmailLoginRequest)
                        }
                    }}
                >
                    <Tabs
                        activeKey={type}
                        onChange={setType}
                        centered
                        items={[
                            {
                                key: 'account',
                                label: '账户密码登录',
                            },
                            {
                                key: 'email',
                                label: '邮箱账号登录',
                            },
                        ]}
                    />

                    {status === 'error' && loginType === 'account' && (
                        <LoginMessage content={'错误的用户名和密码(admin/ant.design)'} />
                    )}
                    {type === 'account' && (
                        <>
                            <ProFormText
                                name="userAccount"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <UserOutlined />,
                                }}
                                placeholder={'请输入账号'}
                                rules={[
                                    {
                                        required: true,
                                        message: '账号是必填项！',
                                    },
                                ]}
                            />
                            <ProFormText.Password
                                name="userPassword"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <LockOutlined />,
                                }}
                                placeholder={'请输入密码'}
                                rules={[
                                    {
                                        required: true,
                                        message: '密码是必填项！',
                                    },
                                ]}
                            />
                        </>
                    )}
                    {type === 'email' && (
                        <>
                            <ProFormText
                                fieldProps={{
                                    size: 'large',
                                    prefix: <MobileOutlined />,
                                }}
                                name="emailAccount"
                                placeholder={'请输入邮箱账号'}
                                rules={[
                                    {
                                        required: true,
                                        message: '邮箱账号是必填项！',
                                    },
                                    {
                                        pattern: /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$/,
                                        message: '不合法的邮箱账号！',
                                    },
                                ]}
                            />
                            <ProFormCaptcha
                                fieldProps={{
                                    size: 'large',
                                    prefix: <LockOutlined />,
                                }}
                                captchaProps={{
                                    size: 'large',
                                }}
                                placeholder={'请输入验证码'}
                                captchaTextRender={(timing, count) => {
                                    if (timing) {
                                        return `${count} ${'秒后重新获取'}`;
                                    }
                                    return '获取验证码';
                                }}
                                phoneName={"emailAccount"}
                                name="captcha"
                                rules={[
                                    {
                                        required: true,
                                        message: '验证码是必填项！',
                                    },
                                ]}
                                onGetCaptcha={async (emailAccount) => {
                                    const res = await getCaptchaUsingGET({ emailAccount })
                                    if (res.data && res.ret === 0) {
                                        message.success("验证码发送成功")
                                        return
                                    }
                                }}
                            />
                        </>
                    )}
                    <div
                        style={{
                            marginBottom: 24,
                        }}
                    >
                        <ProFormCheckbox noStyle name="autoLogin">
                            自动登录
                        </ProFormCheckbox>
                        <Link
                            to={'/user/register'}
                            style={{
                                float: 'right',
                            }}
                        >
                            注册账号
                        </Link>
                        {/* <a
                            style={{
                                float: 'right',
                            }}
                        >
                            忘记密码
                        </a> */}
                    </div>
                </LoginForm>
            </div>
            <Footer />
        </div>
    );
};
export default Login;
