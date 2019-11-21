/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../context/language";
import { MyProfileQuery } from "../../generated/graphql-backend";
import { useLoginState } from "./hooks";
import MY_PROFILE_QUERY from "./profile.graphql";

export const ProfileApp: React.SFC<RouteComponentProps> = () => {
  const [_, setLoginState] = useLoginState(false);
  const lang = useCurrentLanguage();

  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY,
  );

  useEffect(() => {
    const loginUrl = `/${lang}/login`;

    if (error) {
      setLoginState(false);

      navigate(loginUrl);
    }
  }, [error]);

  if (error) {
    return null;
  }

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
      }}
    >
      <h1>
        <FormattedMessage id="profile.header" />
      </h1>

      {loading && "Loading..."}
      {!loading && (
        <dl>
          <dt>
            <FormattedMessage id="profile.email" />
          </dt>
          <dd>{profileData!.me.email}</dd>
        </dl>
      )}
    </Box>
  );
};
