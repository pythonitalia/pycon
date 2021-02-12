import { useEffect } from "react";

import { useRouter } from "next/router";

import { useUser } from "~/hooks/use-user";

const Logout: React.FC = () => {
  const { logout } = useUser();
  const { replace } = useRouter();
  useEffect(() => {
    logout();
    replace("/login");
  }, []);

  return <div></div>;
};

export default Logout;
