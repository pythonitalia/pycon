import { GetStaticPaths, GetStaticProps } from "next";
import Head from "next/head";

import { queryScheduleDays } from "~/types";

export const SchedulePage = () => (
  <Head>
    <meta name="robots" content="noindex, nofollow" />
  </Head>
);

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;
  const {
    data: {
      conference: { days },
    },
  } = await queryScheduleDays({
    code: process.env.conferenceCode,
  });

  const firstDay = days[0].day;
  return {
    redirect: {
      destination: `/${lang}/schedule/${firstDay}/`,
      permanent: false,
    },
  };
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default SchedulePage;
