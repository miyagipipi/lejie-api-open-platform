declare namespace InterfaceInfoAPI {
    type normalResponse = {
        msg: string;
        ret: number;
        data: object;
    }
    
    type RequestParams = {
        userAccount: str
    }

    type InvokeUsingPost = {
        id: number;
        requestParams: RequestParams;
    }

    type Base = {
        id: number;
        name: string | null;
        description: string | null;
        userId: number | null;
        url: number | null;
        method: string | null;
        requestParams: string | null;
        requestHeader: string | null;
        responseHeader: string | null;
        status: number | null;
        createTime: string | null;
        updateTime: string | null;
        totalNum: number | null;
    }

    type AnalysisInterfaceInvokeNumResponse = {
        msg: string;
        ret: number;
        data: Array<Base>;
    }
}