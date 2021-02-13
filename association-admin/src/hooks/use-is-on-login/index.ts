import { useRouter } from "next/router";

export const useIsOnLogin = () => {
  const { pathname } = useRouter();
  return pathname === "/login";
};
