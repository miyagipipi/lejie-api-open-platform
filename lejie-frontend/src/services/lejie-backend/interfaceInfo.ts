// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';


export async function listInterfaceInfoByPageUsingGet(
    body: API.InterfaceInfoPage,
    options?: { [key: string]: any },
) {
    return request<API.InterfaceInfoPageResponse>('/interfaceInfo/page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
        ...(options || {}),
    });
}

export async function addInterfeceInfoUsingPost(
    body: API.InterfaceInfo,
    options?: { [key: string]: any },
) {
    return request<API.BaseResponse>('/interfaceInfo/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
        ...(options || {}),
    });
}

export async function updateInterfeceInfoUsingPost(
    body: API.InterfaceInfo,
    options?: { [key: string]: any },
) {
    return request<API.BaseResponse>('/interfaceInfo/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
        ...(options || {}),
    });
}

export async function deleteInterfeceInfoUsingPost(
    body: API.InterfaceInfoId,
    options?: { [key: string]: any },
) {
    return request<API.BaseResponse>('/interfaceInfo/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
        ...(options || {}),
    });
}

export async function onlineInterfeceInfoUsingPost(
    body: API.IdRequest
) {
    return request<API.BaseResponse>('/interfaceInfo/online', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
    });
}

export async function offlineInterfeceInfoUsingPost(
    body: API.IdRequest
) {
    return request<API.BaseResponse>('/interfaceInfo/offline', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
    });
}

export async function getInterfaceInfoByIdUsingGet(body: API.IdRequest) {
    return request<API.InterfaceInfoNormalResponse>(`/interfaceInfo/getById/${body.id}`, {
        method: 'GET',
    });
}

export async function interfaceInfoInvokeUsingPost(body: InterfaceInfoAPI.InvokeUsingPost) {
    return request<InterfaceInfoAPI.normalResponse>('/interfaceInfo/invoke', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
    });
}

export async function analysisTopInterfaceInvokeUsingGet() {
    return request<InterfaceInfoAPI.AnalysisInterfaceInvokeNumResponse>(`/analysis/interface/top/invoke`, {
        method: 'GET',
    });
}
