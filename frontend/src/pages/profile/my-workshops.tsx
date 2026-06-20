import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryMyProfileWithBookedWorkshops } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({ req }) => {
  const identityToken = req.cookies.pythonitalia_sessionid;
  if (!identityToken) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const client = getApolloClient(null, req.cookies);

  try {
    await Promise.all([
      prefetchSharedQueries(client, DEFAULT_LOCALE),
      queryMyProfileWithBookedWorkshops(client, {
        conference: process.env.conferenceCode,
      }),
    ]);
  } catch {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export { MyWorkshopsProfilePageHandler as default } from "~/components/my-workshops-profile-page-handler";
