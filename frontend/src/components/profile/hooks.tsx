import { updateOlarkFields } from "~/helpers/olark";

export const LOGIN_KEY = "login_state_2";
export const USER_INFO_CACHE = "user_info_cache";

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

  updateOlarkFields();
};

export const useLoginState = () => [getLoginState(), setLoginState];
