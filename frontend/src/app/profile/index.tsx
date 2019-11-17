/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MyProfileQuery } from "../../generated/graphql-backend";
import MY_PROFILE_QUERY from "./profile.graphql";

export const ProfileApp: React.SFC<RouteComponentProps> = () => {
  const { loading, error, data: profileData } = useQuery<MyProfileQuery>(
    MY_PROFILE_QUERY,
  );

  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
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
