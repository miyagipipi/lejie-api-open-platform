declare namespace UserAPI {
    type EmailLoginRequest = {
        captcha?: string;
        emailAccount?: string;
    };

    type RegisterRequest = {
        username: string
        userAccount: string
        userPassword: string
        checkPassword: string
        invitationCode?: string
    }

    type IdRequest = {
        id: number;
    }

    type RegisterResponse = {
        msg: string
        ret: number
        data: IdRequest
    }

    type EmailRegisterRequest = EmailLoginRequest & {
        userName: string
        invitationCode?: string
    }
}