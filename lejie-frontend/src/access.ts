/**
 * @see https://umijs.org/docs/max/access#access
 * */
export default function access(initialState: InitialState | undefined) {
    const { loginUser } = initialState ?? {};
    return {
        canUser: loginUser,
        canAdmin: loginUser?.userRole === 1,
        // canAdmin: currentUser && currentUser.access === 'admin',
    };
}
