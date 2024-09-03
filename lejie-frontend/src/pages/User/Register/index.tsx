import { AlipayCircleOutlined, LinkOutlined, LockOutlined, MailOutlined, RedditOutlined, TaobaoCircleOutlined, UserOutlined, WeiboCircleOutlined } from '@ant-design/icons';
import { Helmet, history, Link } from '@umijs/max';
import { createStyles } from 'antd-style';
import Settings from '../../../../config/defaultSettings';
import React, { useState } from 'react';
import { LoginForm, ProFormCaptcha, ProFormText } from '@ant-design/pro-components';
import { Form, message, Tabs } from 'antd';
import { getCaptchaUsingGET, userEmailRegisterUsingPOST, userRegisterUsingPOST } from '@/services/lejie-backend/user';

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
        container: {
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            overflow: 'auto',
            backgroundImage:
                "url('https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/V-_oS6r-i7wAAAAAAAAAAAAAFl94AQBr')",
            backgroundSize: '100% 100%',
        }
    }
})

const ActionIcons = () => {
    const { styles } = useStyles()

    return (
        <>
            <AlipayCircleOutlined key="AlipayCircleOutlined" className={styles.action}></AlipayCircleOutlined>
            <TaobaoCircleOutlined key="TaobaoCircleOutlined" className={styles.action}></TaobaoCircleOutlined>
            <WeiboCircleOutlined key="WeiboCircleOutlined" className={styles.action}></WeiboCircleOutlined>
        </>
    )
}

const Register: React.FC = () => {
    const { styles } = useStyles();
    const [type, setType] = useState<string>('account')
    const [invitationCode, setInvitationCode] = useState<string>('');
    const [form] = Form.useForm()
    const [messageApi, contextHolder] = message.useMessage();

    const doRegister = (res: UserAPI.RegisterResponse) => {
        if (res.ret === 0 && res.data) {
            message.success('注册成功！');
            setTimeout(() => {
                history.push('/user/login')
            }, 1000);
            return;
        } else {
            message.error(res.msg)
            return
        }
    }

    const handleSubmit = async (values: UserAPI.RegisterRequest) => {
        if (values.userPassword !== values.checkPassword) {
            messageApi.error('两次密码不一致，请检查')
            return
        }
        const res = await userRegisterUsingPOST({...values})
        doRegister(res)
    }

    const handleEmailSubmit = async (values: UserAPI.EmailRegisterRequest) => {
        const res = await userEmailRegisterUsingPOST({...values})
        doRegister(res)
    }

    return (
        <div className={styles.container}>
            {contextHolder}
            <Helmet>
                <title>
                    {'注册'}- {Settings.title}
                </title>
            </Helmet>
            <div
                style={{
                    flex: '1',
                    padding: '32px 0',
                }}
            >
                <LoginForm
                    form={form}
                    submitter={
                        {
                            searchConfig: {
                                submitText: "注册"
                            }
                        }
                    }
                    contentStyle={{
                        minWidth: 280,
                        maxWidth: '75vw'
                    }}
                    logo={<img alt="logo" src="/logo.svg" />}
                    title={Settings.title}
                    subTitle={'致力于提供稳定、安全、高效的接口调用服务'}
                    actions={['其他登录方式 :', <ActionIcons key="icons" />]}
                    initialValues={{
                        invitationCode: invitationCode
                    }}
                    onFinish={async (values) => {
                        if (type === 'account') {
                            await handleSubmit(values as UserAPI.RegisterRequest);
                        } else {
                            await handleEmailSubmit(values as UserAPI.EmailRegisterRequest)
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
                                label: '账户密码注册',
                            },
                            {
                                key: 'email',
                                label: '邮箱账号注册',
                            },
                        ]}
                    />
                    {type === 'account' && (
                        <>
                            <ProFormText
                                name="username"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <RedditOutlined />,
                                }}
                                placeholder={'请输入昵称'}
                            />
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
                                        message: '账号是必填项！'
                                    }
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
                            <ProFormText.Password
                                name="checkPassword"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <LockOutlined />,
                                }}
                                placeholder={'再次输入密码'}
                                rules={[
                                    {
                                        required: true,
                                        message: '密码是必填项！',
                                    },
                                ]}
                            />
                            <ProFormText
                                name="invitationCode"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <LinkOutlined />,
                                }}
                                placeholder={'请输入邀请码,没有可不填'}
                            />
                        </>
                    )}
                    {type === 'email' && (
                        <>
                            <ProFormText
                                name="username"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <RedditOutlined />,
                                }}
                                placeholder={'请输入昵称'}
                            />
                            <ProFormText
                                name="emailAccount"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <MailOutlined />,
                                }}
                                placeholder={'请输入邮箱'}
                                rules={[
                                    {
                                        required: true,
                                        message: '邮箱是必填项！'
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
                                // 手机号的 name，onGetCaptcha 会注入这个值
                                phoneName="emailAccount"
                                name="captcha"
                                rules={[
                                    {
                                        required: true,
                                        message: '请输入验证码',
                                    },
                                ]}
                                placeholder="请输入验证码"
                                // 如果需要失败可以 throw 一个错误出来，onGetCaptcha 会自动停止
                                // throw new Error("获取验证码错误")
                                onGetCaptcha={async (emailAccount) => {
                                    const res = await getCaptchaUsingGET({emailAccount})
                                    if (res.data && res.ret === 0) {
                                        message.success(`验证码发送成功!`);
                                    } else {
                                        message.error(res.msg)
                                    }
                                }}
                            />
                            <ProFormText
                                name="invitationCode"
                                fieldProps={{
                                    size: 'large',
                                    prefix: <LinkOutlined />,
                                }}
                                placeholder={'请输入邀请码,没有可不填'}
                            />
                        </>
                    )}
                    <div
                        style={{
                            marginBottom: 54
                        }}
                    >
                        <Link
                            to={'/user/login'}
                            style={{
                                float: 'right',
                            }}
                        >
                            已有账号? 点击前往登录
                        </Link>
                    </div>
                </LoginForm>
            </div>
        </div>
    )
}

export default Register
