import Head from "next/head";
import { useRouter } from "next/router";
import React, { Fragment, useEffect } from "react";

import { getInitialLocale } from "~/locale/get-initial-locale";

export const HomeNoLang = () => {
  const router = useRouter();
  useEffect(() => {
    router.replace("/[lang]", `/${getInitialLocale()}`);
    // window.location.href = `/${getInitialLocale()}`;
  }, []);

  return (
    <Fragment>
      <Head>
        <meta name="robots" content="noindex, nofollow" />
      </Head>
    </Fragment>
  );
};

export default HomeNoLang;
