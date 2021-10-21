import { GetServerSideProps } from "next";
import cookies from "next-cookies";
import Head from "next/head";

import { DEFAULT_LOCALE } from "~/locale/languages";

export const HomeNoLang = () => (
  <Head>
    <meta name="robots" content="noindex, nofollow" />
  </Head>
);

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { pyconLocale } = cookies(context);
  const res = context.res;
  res.setHeader("location", `/${pyconLocale || DEFAULT_LOCALE}`);
  res.statusCode = 302;
  res.end();
  return {
    props: {},
  };
};

export default HomeNoLang;
