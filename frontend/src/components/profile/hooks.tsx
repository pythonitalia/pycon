export const LOGIN_KEY = "login_state_2";

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

export const setLoginState = (value: boolean) =>
  window.localStorage.setItem(LOGIN_KEY, JSON.stringify(value));

export const useLoginState = () => [getLoginState(), setLoginState];
