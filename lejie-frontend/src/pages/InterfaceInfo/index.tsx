import { getInterfaceInfoByIdUsingGet, interfaceInfoInvokeUsingPost } from '@/services/lejie-backend/interfaceInfo';
import { PageContainer } from '@ant-design/pro-components';
import { useParams } from '@umijs/max';
import { Button, Card, Descriptions, DescriptionsProps, Divider, Form, message } from 'antd';
import TextArea from 'antd/es/input/TextArea';
import React, { useEffect, useState } from 'react';


type FieldType = {
    requestParams: string;
};

/**
 * 主页
 * @constructor 
 */
const Welcome: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<API.InterfaceInfo>();
    const [invokeRes, setInvokeRes] = useState<any>();
    const [invokeLoading, setInvokeLoading] = useState(false);
    const params = useParams()

    const items: DescriptionsProps['items'] = [
        {
            key: 'status',
            label: '接口状态',
            children: <p>{data?.status ? '正常' : '关闭'}</p>,
        },
        {
            key: 'description',
            label: '描述',
            children: <p>{data?.description}</p>,
        },
        {
            key: 'url',
            label: '请求地址',
            children: <p>{data?.url}</p>,
        },

        {
            key: 'method',
            label: '请求方法',
            children: <p>{data?.method}</p>,
        },
        {
            key: 'requestParams',
            label: '请求参数',
            children: <p>{data?.requestParams}</p>,
        },
        {
            key: 'requestHeader',
            label: '请求头',
            children: <p>{data?.requestHeader}</p>,
        },
        {
            key: 'responseHeader',
            label: '响应头',
            children: <p>{data?.responseHeader}</p>,
        },
        {
            key: 'createTime',
            label: '创建时间',
            children: <p>{data?.createTime?.replaceAll('T', ' ')}</p>,
        },
        {
            key: 'updateTime',
            label: '更新时间',
            children: <p>{data?.updateTime?.replaceAll('T', ' ')}</p>,
        },
    ]

    /**
     * 
     * @param current 第几页
     * @param pageSize 每页多少条
     * @returns 
     */
    const loadData = async () => {
        if (!params.id) {
            message.error('参数不存在');
            return
        }
        setLoading(true)
        try {
            const res = await getInterfaceInfoByIdUsingGet({
                id: Number(params.id)
            })
            setData(res.data)
        } catch (error: any) {
            message.error('请求失败: ' + error.message);
        }
        setLoading(false)
    }
    useEffect(() => {
        loadData()
    }, [])

    const onFinish = async (values: FieldType) => {
        if (!params.id) {
            message.error('接口已停用')
            return
        }
        setInvokeLoading(true)
        try {
            const res = await interfaceInfoInvokeUsingPost({
                requestParams: JSON.parse(values.requestParams),
                id: Number(params.id),
            })
            if (res.ret === 0) {
                setInvokeRes(res.msg)
                message.success('调用成功')
            }
        } catch (error: any) {
            message.error('操作失败: ' + error.message)
        }
        setInvokeLoading(false)
    };

    return (
        <PageContainer title="查看接口文档">
            <Card>
                <Descriptions title={data?.name} items={items} column={1} />
            </Card>
            <Divider></Divider>
            <Card title="在线调用">
                <Form
                    name="invoke"
                    layout="vertical"
                    onFinish={onFinish}
                >
                    <Form.Item<FieldType>
                        label="请求参数"
                        name="requestParams"
                    >
                        <TextArea></TextArea>
                    </Form.Item>
                    <Form.Item wrapperCol={{ span: 16 }}>
                        <Button type="primary" htmlType="submit">
                            调用
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
            <Divider></Divider>
            <Card title="调用结果" loading={invokeLoading}>
                {invokeRes}
            </Card>
        </PageContainer>
    );
};

export default Welcome;
