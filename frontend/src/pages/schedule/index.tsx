import { GetStaticProps } from "next";
import Head from "next/head";

import { getApolloClient } from "~/apollo/client";
import { queryScheduleDays } from "~/types";

export const SchedulePage = () => (
  <Head>
    <meta name="robots" content="noindex, nofollow" />
  </Head>
);

export const getStaticProps: GetStaticProps = async ({}) => {
  const client = getApolloClient();
  const {
    data: {
      conference: { days },
    },
  } = await queryScheduleDays(client, {
    code: process.env.conferenceCode,
  });

  const firstDay = days[0].day;
  return {
    redirect: {
      destination: `/schedule/${firstDay}/`,
      permanent: false,
    },
  };
};

export default SchedulePage;
