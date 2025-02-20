import type { GetServerSideProps } from "next";

import { getApolloClient } from "~/apollo/client";
import { queryTicketIdToHashid } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
}) => {
  const hashid = params.hashid as string;
  const client = getApolloClient(null, req.cookies);
  const result = await queryTicketIdToHashid(client, {
    ticketId: hashid,
    conference: process.env.conferenceCode,
  });

  if (result.data?.ticketIdToHashid) {
    return {
      redirect: {
        destination: `/profile/${result.data.ticketIdToHashid}`,
        permanent: false,
      },
    };
  }

  return {
    notFound: true,
  };
};

export default () => {
  return <div>temporary!</div>;
};
