import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryMyProfileWithOrders } from "~/types";

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
      queryMyProfileWithOrders(client, {
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

export { MyOrdersProfilePageHandler as default } from "~/components/my-orders-profile-page-handler";
