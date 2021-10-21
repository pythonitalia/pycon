/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import Router from "next/router";

import { addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { useLoginState } from "~/components/profile/hooks";
import { Logout } from "~/components/profile/logout";
import { MyOrders } from "~/components/profile/my-orders";
import { MyProfile } from "~/components/profile/my-profile";
import { MySubmissions } from "~/components/profile/my-submissions";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryCountries, useMyProfileQuery } from "~/types";

export const MyProfilePage = () => {
  const [loggedIn, setLoginState] = useLoginState();
  const lang = useCurrentLanguage();

  const {
    loading,
    error,
    data: profileData,
  } = useMyProfileQuery({
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

  useEffect(() => {
    if (!loggedIn) {
      const loginUrl = `/${lang}/login`;
      setLoginState(false);
      Router.push("/[lang]/login", loginUrl);
    }
  }, []);

  if (loading) {
    return <PageLoading titleId="profile.title" />;
  }

  if (error) {
    return (
      <Alert variant="alert">Ops, something went wrong: {error.message}</Alert>
    );
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

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await Promise.all([prefetchSharedQueries(lang), queryCountries()]);

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default MyProfilePage;
