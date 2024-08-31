// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Usercreate POST /user/create/ */
export async function userCreatePost(
    body: API.UserCreate,
    options?: { [key: string]: any },
) {
    return request<API.User>('/user/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body,
        ...(options || {}),
    });
}

/** Usergetuserbyid GET /user/getUserById/${param0} */
export async function userGetUserByIdGet(
    // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
    params: API.userGetUserByIdParams,
    options?: { [key: string]: any },
) {
    const { user_id: param0, ...queryParams } = params;
    return request<API.User>(`/user/getUserById/${param0}`, {
        method: 'GET',
        params: { ...queryParams },
        ...(options || {}),
    });
}

/** Usertoken POST /user/token */
export async function userTokenPost(
    body: API.UserToken,
    options?: { [key: string]: any },
) {
    return request<API.UserTokenResponse>('/user/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: body, 
        ...(options || {}),
    });
}

export async function userCurrentGet() {
    return request<API.UserResponse>('/user/current', {
        method: 'GET',
    });
}
