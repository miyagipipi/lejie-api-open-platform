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
        /** Username */
        username: string;
        /** Useraccount */
        userAccount: string;
        /** Userpassword */
        userPassword: string;
        /** Gender */
        gender: number;
        /** Phone */
        phone: string;
        /** Email */
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
        /** Location */
        loc: (string | number)[];
        /** Message */
        msg: string;
        /** Error Type */
        type: string;
    };

    type UserToken = {
        /** Useraccount */
        username: string;
        password: string;
    };

    type UserTokenResponse = {
        access_token: string;
        token_type: string;
        ret: number;
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

    type InterfaceInfoResponse = {
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
}
