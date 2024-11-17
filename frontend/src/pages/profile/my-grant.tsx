import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryCountries,
  queryMyProfileWithGrant,
  queryParticipantData,
} from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
}) => {
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
      prefetchSharedQueries(client, locale),
      queryCountries(client),
      queryMyProfileWithGrant(client, {
        conference: process.env.conferenceCode,
      }),
      queryParticipantData(client, {
        conference: process.env.conferenceCode,
      }),
    ]);
  } catch (e) {
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

export { MyGrantProfilePageHandler as default } from "~/components/my-grant-profile-page-handler";
