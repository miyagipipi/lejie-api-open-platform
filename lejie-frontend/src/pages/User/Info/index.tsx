import { EditOutlined } from '@ant-design/icons';
import { ProCard } from '@ant-design/pro-components';
import { useModel } from '@umijs/max';
import { Button, Descriptions, message, Spin, Tooltip, Tour, TourProps } from 'antd';
import Paragraph from 'antd/es/typography/Paragraph';
import React, { useEffect, useRef, useState } from 'react';
import EmailModal from '@/components/EmailModal'
import { userEmailBindUsingPOST, userEmailUnBindUsingPOST } from '@/services/lejie-backend/user';
import { InitialStateType } from '@/.umi/plugin-initialState/@@initialState';

export const valueLength = (val: any) => {
    return val && val.trim().length > 0
}

const UserInfo: React.FC = () => {
    const [loading, setLoading] = useState(true)
    const { initialState, setInitialState } = useModel('@@initialState');
    const {loginUser} = initialState || {}
    const [userName, setUserName] = useState<string | undefined | null>('')
    const [openEmailModal, setOpenEmailModal] = useState(false)

    const ref1 = useRef(null)
    const ref2 = useRef(null);
    const ref3 = useRef(null);
    const ref4 = useRef(null);

    const steps: TourProps['steps'] = [
        {
            title: '个人信息设置',
            description: <span>这里是你的账号信息，您可以便捷的查看您的基本信息。<br />您还可以修改和更新昵称和头像。
                <br />邮箱主要用于接收<strong>支付订单信息</strong>，不绑定无法接收哦，快去绑定吧！！🥰</span>,
            target: () => ref1.current,
        },
        {
            title: '我的钱包',
            description: <span>这里是您的钱包，坤币用于平台接口的调用费用。<br />除了充值坤币外，您还可以每日签到或者邀请好友注册来获得坤币</span>,
            target: () => ref2.current,
        },
        {
            title: '接口调用凭证',
            description: '这里是您调用接口的凭证，没有凭证将无法调用接口',
            target: () => ref3.current,
        },
        {
            title: '开发者SDK',
            description: '您可以使用开发者SDK，快速高效的接入接口到您的项目中',
            target: () => ref4.current,
        }
    ]

    const loadData = async () => {
        setLoading(true)
        
        setUserName(loginUser?.username)

        setLoading(false)
    }

    useEffect(() => {
        loadData()
    }, [])

    const handleBindEmailSubmit = async (values: UserAPI.EmailBindRequest) => {
        const res = await userEmailBindUsingPOST({...values})
        if (res.ret === 0 && res.data) {
            const newInitialState: InitialStateType  = {
                ...initialState,
                loginUser: {
                    ...initialState?.loginUser,
                    email: res.data.emailAccount
                } as API.User
            }
            setInitialState(newInitialState)
            message.success('绑定成功')
            setOpenEmailModal(false)
        }
    };

    return (
        <Spin spinning={loading}>
            <ProCard
                type='inner'
                bordered
                direction='column'
            >
                <ProCard
                    ref={ref1}
                    extra={
                        <>
                            <Tooltip title={"用于接收订单信息"}
                            >
                                <Button onClick={() => {
                                    setOpenEmailModal(true)
                                }}>
                                    {initialState?.loginUser?.email ? "换绑邮箱" : "绑定邮箱"}
                                </Button>
                            </Tooltip>
                            <Tooltip title={"提交修改信息"}>
                                <Button
                                    style={{marginLeft: 10}}
                                    onClick={() => {
                                        // updateUserInfo
                                }}>提交修改
                                </Button>
                            </Tooltip>
                        </>
                    }
                    title={<strong>个人信息设置</strong>}
                    type='inner'
                    bordered
                >
                    <Descriptions column={1}>
                        <div>
                            <h4>昵称：</h4>
                            <Paragraph
                                editable={
                                    {
                                        icon: <EditOutlined />,
                                        tooltip: '编辑',
                                        onChange: (value: any) => {
                                            setUserName(value)
                                        }
                                    }
                                }>
                                {valueLength(userName) ? userName : 'unknow user'}
                            </Paragraph>
                        </div>
                        <div>
                            <Tooltip title={'邀请好友注册，双方各得100积分'}></Tooltip>
                        </div>
                        <div>
                            <h4>我的ID: </h4>
                            <Paragraph>{loginUser?.id}</Paragraph>
                        </div>
                        <div>
                            <h4>我的邮箱: </h4>
                            <Paragraph copyable={valueLength(loginUser?.email)}>
                                {valueLength(loginUser?.email) ? loginUser?.email : '未绑定邮箱'}
                            </Paragraph>
                        </div>
                    </Descriptions>
                </ProCard>
            </ProCard>
            <EmailModal
                open={openEmailModal}
                onCancel={() => setOpenEmailModal(false)}
                data={loginUser}
                bindSubmit={handleBindEmailSubmit}
            />
        </Spin>
    )

    
}

export default UserInfo
