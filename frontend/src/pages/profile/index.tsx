import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryCountries, queryMyProfile } from "~/types";

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

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryCountries(client),
    queryMyProfile(client),
  ]);

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export { ProfilePageHandler as default } from "~/components/profile-page-handler";
