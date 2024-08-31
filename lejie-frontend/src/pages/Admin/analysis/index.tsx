import {
    PageContainer,
} from '@ant-design/pro-components';
import '@umijs/max';
import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { analysisTopInterfaceInvokeUsingGet } from '@/services/lejie-backend/interfaceInfo';


const InterfaceAnalysis: React.FC = () => {

    const [data, setData] = useState<InterfaceInfoAPI.Base[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        analysisTopInterfaceInvokeUsingGet().then(response => {
            if (response.data) {
                setData(response.data)
                setLoading(false)
            }
        })
    }, [])

    // 映射: {value: totalNum, name: name}
    const chartData = data.map(item => {
        return {
            value: item.totalNum,
            name: item.name
        }
    })

    const option = {
        title: {
          text: '调用次数 Top3 的接口',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: chartData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };

    return (
        <PageContainer>
            <ReactECharts option={option} showLoading={loading} />
        </PageContainer>
    );
};
export default InterfaceAnalysis;
