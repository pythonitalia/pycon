import Head from "next/head";
import { useRouter } from "next/router";
import React from "react";

import { getInitialLocale } from "~/locale/get-initial-locale";

export const HomeNoLang = () => {
  const router = useRouter();

  React.useEffect(() => {
    router.replace("/[lang]", `/${getInitialLocale()}`);
  }, []);

  return (
    <Head>
      <meta name="robots" content="noindex, nofollow" />
    </Head>
  );
};

export default HomeNoLang;
