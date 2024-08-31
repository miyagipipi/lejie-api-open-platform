import { listInterfaceInfoByPageUsingGet } from '@/services/lejie-backend/interfaceInfo';
import { PageContainer } from '@ant-design/pro-components';
import { List, message } from 'antd';
import React, { useEffect, useState } from 'react';


/**
 * 主页
 * @constructor 
 */
const Welcome: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [list, setList] = useState<API.InterfaceInfo[]>([]);
    const [total, setTotal] = useState<number>(0)

    /**
     * 
     * @param current 第几页
     * @param pageSize 每页多少条
     * @returns 
     */
    const loadData = async (current: number = 1, pageSize: number = 10) => {
        setLoading(true)
        try {
            const res = await listInterfaceInfoByPageUsingGet({
                current,
                pageSize
            })
            setList(res.data)
            setTotal(res.total)
        } catch (error: any) {
            message.error('请求失败: ' + error.message);
        }
        setLoading(false)
    }
    useEffect(() => {
        loadData()
    }, [])

    return (
        <PageContainer title="接口开放平台">
            <List
                className="my-list"
                loading={loading}
                itemLayout="horizontal"
                dataSource={list}
                renderItem={(item) => {
                    const apiLink = `/interfaceInfo/${item.id}`;
                    return <List.Item actions={[<a key={`list-edit-${item.id}`} href={apiLink}>查看</a>]}>
                        <List.Item.Meta
                            title={<a href={apiLink}>{item.name}</a>}
                            description={item.description}
                        />
                    </List.Item>
                }}
                pagination={
                    {
                        showTotal(total) { return `总数: ${total}` },
                        pageSize: 10,
                        total,
                        onChange(page, pageSize) {
                            loadData(page, pageSize)
                        }
                    }
                }
            />
        </PageContainer>
    );
};

export default Welcome;
