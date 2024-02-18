export const LOGIN_KEY = "login_state_v3";
export const USER_INFO_CACHE = "user_info_cache_v2";

const getLoginState = () => {
  const value =
    typeof window === "undefined"
      ? null
      : window.localStorage.getItem(LOGIN_KEY);

  if (!value) {
    return false;
  }

  try {
    return JSON.parse(value);
  } catch {
    return false;
  }
};

export const setLoginState = (value: boolean) => {
  window.localStorage.setItem(LOGIN_KEY, JSON.stringify(value));

  if (!value) {
    window.localStorage.removeItem(USER_INFO_CACHE);
  }
};

export const useLoginState = () => [getLoginState(), setLoginState];
