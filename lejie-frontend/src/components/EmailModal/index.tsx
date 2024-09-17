import { getCaptchaUsingGET } from "@/services/lejie-backend/user";
import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { LoginForm, ProFormCaptcha, ProFormInstance, ProFormText } from "@ant-design/pro-components";
import { Button, message, Modal } from "antd";
import React, { useEffect, useRef, useState } from "react"


export type Props = {
    open: boolean;
    onCancel: () => void;
    data?: API.User;
    bindSubmit: (values: UserAPI.EmailBindRequest) => Promise<void>;
}

const EmailModal: React.FC<Props> = (props) => {
    const formRef = useRef<ProFormInstance>()
    const [key, setKey] = useState<"bind" | "unbind">()
    const { open, data, onCancel, bindSubmit } = props

    useEffect(() => {
        if (!open) {
            formRef.current?.resetFields()
        }
    }, [open])

    return (
        <Modal
            footer={null}
            centered
            open={open}
            width={500}
            onCancel={onCancel}
        >
            <LoginForm
                formRef={formRef}
                contentStyle={{
                    minWidth: 280,
                    maxWidth: '750vw'
                }}
                submitter={
                    {
                        render: () => {
                            return [
                                <>
                                    <Button
                                        type={"primary"}
                                        key="submit"
                                        block
                                        onClick={() => {
                                            setKey("bind")
                                            formRef.current?.submit()
                                        }}
                                    >
                                        {data?.email ? '更新邮箱' : '绑定邮箱'}
                                    </Button>
                                </>
                            ]
                        }
                    }
                }
                onFinish={async (values: any) => {
                    bindSubmit?.(values)
                }}
            >
                <ProFormText
                    fieldProps={{
                        size: 'large',
                        prefix: <MailOutlined />
                    }}
                    name="emailAccount"
                    placeholder={'请输入邮箱账号！'}
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
                >
                </ProFormText>
                <ProFormCaptcha
                    fieldProps={{
                        size: 'large',
                        prefix: <LockOutlined />,
                    }}
                    captchaProps={{
                        size: 'large',
                    }}
                    placeholder={'请输入验证码！'}
                    captchaTextRender={(timing: boolean, count: number) => {
                        if (timing) {
                            return `${count} 秒后重新获取`
                        }
                        return '获取验证码'
                    }}
                    phoneName={"emailAccount"}
                    name={"captcha"}
                    rules={[
                        {
                            required: true,
                            message: '验证码是必填项！',
                        },
                    ]}
                    onGetCaptcha={async (emailAccount: string) => {
                        const res = await getCaptchaUsingGET({
                            emailAccount
                        })
                        if (res.ret === 0) {
                            message.success('验证码发送成功')
                            return
                        }
                    }}
                >
                </ProFormCaptcha>
            </LoginForm>
        </Modal>
    )
}

export default EmailModal
