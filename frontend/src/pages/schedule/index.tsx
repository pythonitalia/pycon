import { GetServerSideProps } from "next";

import { getApolloClient } from "~/apollo/client";
import { queryScheduleDays } from "~/types";

const ScheduleIndex = () => {
  return null;
};

export const getServerSideProps: GetServerSideProps = async () => {
  // TODO Convert to _middleware
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
      permanent: false,
      destination: `/schedule/${firstDay}`,
    },
  };
};

export default ScheduleIndex;
