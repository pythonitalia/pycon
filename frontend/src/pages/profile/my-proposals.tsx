import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryMyProfileWithSubmissions } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
}) => {
  const identityToken = req.cookies["identity_v2"];
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
      queryMyProfileWithSubmissions(client, {
        conference: process.env.conferenceCode,
        language: locale,
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

export { MyProposalsProfilePageHandler as default } from "~/components/my-proposals-profile-page-handler";
