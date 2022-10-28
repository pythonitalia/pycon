/** @jsxRuntime classic */

/** @jsx jsx */
import { useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "~/components/profile/hooks";

import { Link } from "../link";

export const ProfileLink = () => {
  const [loggedIn] = useLoginState();
  const [firstRender, setFirstRender] = useState(true);

  useEffect(() => {
    if (firstRender) {
      setFirstRender(false);
    }
  }, []);

  return (
    <Link
      path={!firstRender && loggedIn ? "/profile" : "/login"}
      variant="arrow-button"
      sx={{
        mr: 2,
        display: ["none", "block"],
        maxWidth: "138px",
        width: "100%",
      }}
    >
      {!firstRender && loggedIn && <FormattedMessage id="header.profile" />}
      {(firstRender || !loggedIn) && <FormattedMessage id="header.login" />}
    </Link>
  );
};
