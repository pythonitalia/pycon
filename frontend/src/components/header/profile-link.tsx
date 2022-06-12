/** @jsxRuntime classic */

/** @jsx jsx */
import { useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "~/components/profile/hooks";

import { Link } from "../link";

export const ProfileLink = () => {
  const [loggedIn] = useLoginState();
  const [firstRender, setFirstRender] = useState(false);

  useEffect(() => {
    if (firstRender) {
      setFirstRender(false);
    }
  }, []);

  return (
    <Link
      path={!firstRender && loggedIn ? "/profile" : "/login"}
      variant="arrow-button"
      sx={{ mr: 4, display: ["none", "block"] }}
    >
      {!firstRender && loggedIn && <FormattedMessage id="header.profile" />}
      {firstRender || (!loggedIn && <FormattedMessage id="header.login" />)}
    </Link>
  );
};
