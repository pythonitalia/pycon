import { useRouter } from "next/dist/client/router";
import Head from "next/head";
import React from "react";

import { getInitialLocale } from "~/locale/get-initial-locale";

export default () => {
  const router = useRouter();

  React.useEffect(() => {
    router.replace("/[lang]", `/${getInitialLocale()}`);
  });

  return (
    <Head>
      <meta name="robots" content="noindex, nofollow" />
    </Head>
  );
};
