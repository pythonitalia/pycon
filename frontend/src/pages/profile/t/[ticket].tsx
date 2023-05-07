import { GetServerSideProps } from "next";

import { getApolloClient } from "~/apollo/client";

export const getServerSideProps: GetServerSideProps = async ({
  locale,
  req,
  params,
}) => {
  const client = getApolloClient(null, req.cookies);
  // todo:
  // take the ticket id (which is the order position)
  // get the user hash id from it
  // redirect to the public profile page (/profile/[hashid])
};
