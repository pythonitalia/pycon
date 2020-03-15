/** @jsx jsx */
import { Box } from "@theme-ui/components";
import Router from "next/router";
import { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { Logout } from "~/app/profile/logout";
import { MyOrders } from "~/app/profile/my-orders";
import { MyProfile } from "~/app/profile/my-profile";
import { MySubmissions } from "~/app/profile/my-submissions";
import { Alert } from "~/components/alert";
import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileQuery } from "~/types";

export default () => {
  const [loggedIn, setLoginState] = useLoginState();
  const lang = useCurrentLanguage();

  const { loading, error, data: profileData } = useMyProfileQuery({
    skip: !loggedIn,
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  useEffect(() => {
    const loginUrl = `/${lang}/login`;

    if (error) {
      setLoginState(false);

      Router.push(loginUrl);
    }
  }, [error]);

  if (loading) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Alert variant="info">
            <FormattedMessage id="profile.loading" />
          </Alert>
        )}
      </Box>
    );
  }

  if (error || !profileData) {
    return null;
  }

  return (
    <Fragment>
      <MyProfile profile={profileData} />

      {profileData.me.orders.length > 0 && (
        <MyOrders orders={profileData.me.orders} />
      )}

      <MySubmissions
        sx={{
          borderTop: "primary",
          mb: 4,

          "> div": {
            px: 3,
          },
        }}
      />
      <Logout />
    </Fragment>
  );
};
