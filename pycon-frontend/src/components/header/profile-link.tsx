/** @jsxRuntime classic */
/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";

import { Link } from "../link";

export const ProfileLink = () => {
  const [loggedIn] = useLoginState();

  return (
    <Link
      path={loggedIn ? "/[lang]/profile" : "/[lang]/login"}
      variant="arrow-button"
      sx={{ mr: 5, display: ["none", "block"] }}
    >
      {loggedIn && <FormattedMessage id="header.profile" />}
      {!loggedIn && <FormattedMessage id="header.login" />}
    </Link>
  );
};
