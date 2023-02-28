import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryCountries, queryMyEditProfile } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  locale,
  req,
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
    queryMyEditProfile(client),
  ]);

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export { EditProfilePageHandler as default } from "../../components/edit-profile-page-handler";
