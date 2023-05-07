import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryParticipantPublicProfile } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  locale,
  req,
  params,
}) => {
  const client = getApolloClient(null, req.cookies);

  try {
    await Promise.all([
      prefetchSharedQueries(client, locale),
      queryParticipantPublicProfile(client, {
        conference: process.env.conferenceCode,
        userId: params.hashid as string,
      }),
    ]);
  } catch (e) {
    return {
      notFound: true,
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

export { PublicProfilePageHandler as default } from "../../components/public-profile-page-handler";
