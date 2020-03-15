import { useRouter } from "next/dist/client/router";
import Head from "next/head";
import React from "react";

import { useCurrentLanguage } from "~/locale/context";

export default () => {
  const router = useRouter();
  const language = useCurrentLanguage();

  // TODO: from backend

  React.useEffect(() => {
    router.replace(`/${language}/schedule/2020-11-06`);
  });

  return (
    <Head>
      <meta name="robots" content="noindex, nofollow" />
    </Head>
  );
};
