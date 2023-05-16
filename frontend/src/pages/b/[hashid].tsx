import { GetServerSideProps } from "next";

import { getApolloClient } from "~/apollo/client";
import { queryTicketIdToUserHashid } from "~/types";

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
}) => {
  const hashid = params.hashid as string;
  const client = getApolloClient(null, req.cookies);
  const result = await queryTicketIdToUserHashid(client, {
    ticketId: hashid,
    conference: process.env.conferenceCode,
  });

  if (result.data?.ticketIdToUserHashid) {
    return {
      redirect: {
        destination: `/profile/${result.data.ticketIdToUserHashid}`,
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
