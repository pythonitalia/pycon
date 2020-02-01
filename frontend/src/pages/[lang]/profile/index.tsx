/** @jsxRuntime classic */
/** @jsx jsx */
import Router from "next/router";
import { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { useLoginState } from "~/components/profile/hooks";
import { Logout } from "~/components/profile/logout";
import { MyOrders } from "~/components/profile/my-orders";
import { MyProfile } from "~/components/profile/my-profile";
import { MySubmissions } from "~/components/profile/my-submissions";
import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileQuery } from "~/types";

export const MyProfilePage = () => {
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

      Router.push("/[lang]/login", loginUrl);
    }
  }, [error]);

  if (loading) {
    return <PageLoading titleId="profile.title" />;
  }

  if (error) {
    throw error;
  }

  if (!profileData) {
    return null;
  }

  return (
    <Fragment>
      <FormattedMessage id="profile.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

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

export default MyProfilePage;
