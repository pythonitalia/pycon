import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryParticipantPublicProfile } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
}) => {
  const client = getApolloClient(null, req.cookies);

  try {
    const [_, participantQuery] = await Promise.all([
      prefetchSharedQueries(client, DEFAULT_LOCALE),
      queryParticipantPublicProfile(client, {
        conference: process.env.conferenceCode,
        id: params.hashid as string,
        language: DEFAULT_LOCALE,
      }),
    ]);

    if (participantQuery.data.participant === null) {
      return {
        notFound: true,
      };
    }
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
