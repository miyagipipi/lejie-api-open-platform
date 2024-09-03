declare namespace API {
    type HTTPValidationError = {
        /** Detail */
        detail?: ValidationError[];
    };

    type User = {
        username?: string | null;
        userAccount: string | null;
        avatarUrl: string | null;
        gender?: number | null;
        phone: string | null;
        email: string | null;
        tags?: string | null;
        profile: string | null;
        createTime?: string | null;
        userRole: number | null;
        id: number;
    };

    type UserCreate = {
        username: string;
        userAccount: string;
        userPassword: string;
        gender: number;
        phone: string;
        email: string;
    };

    type userGetUserByIdParams = {
        user_id: number;
    };

    type UserLogin = {
        userAccount: string;
        userPassword: string;
    };

    type UserResponse = {
        msg: string;
        ret: number;
        data: User
    }

    type ValidationError = {
        loc: (string | number)[];
        msg: string;
        type: string;
    };

    type UserToken = {
        username: string;
        password: string;
    };

    type UserTokenResponse = {
        access_token: string;
        token_type: string;
        ret: number;
    }

    type EmailLoginTokenResponse = {
        msg: string;
        ret: number;
        data: UserTokenResponse;
    }

    type InterfaceInfo = {
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
        // isDelete: number | null;
    }

    type InterfaceInfoId = {
        id: number;
    }

    type InterfaceInfoPage = {
        pageSize?: number;
        current?: number;
        keyword?: string;
    }

    type InterfaceInfoPageResponse = {
        msg: string;
        ret: number;
        total: number;
        data: Array<InterfaceInfo>;
    }

    type BaseResponse = {
        msg: string;
        ret: number;
        data?: object;
    }

    type IdRequest = {
        id: number;
    }

    type InterfaceInfoNormalResponse = {
        msg: string;
        ret: number;
        data: InterfaceInfo;
    }

    type getCaptchaUsingGETParams = {
        emailAccount: string;
    }
}
