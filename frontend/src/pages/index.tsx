import Head from "next/head";
import { useRouter } from "next/router";
import React from "react";

import { getBestLanguageForUser } from "~/helpers/get-best-language-for-user";
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

HomeNoLang.getInitialProps = async ({ req, res }) => {
  if (!req) {
    return {};
  }

  // TODO: Convert user selection of language from localStorage to cookie
  // so we can read it here

  const acceptLanguage = req.headers["accept-language"];

  if (!acceptLanguage) {
    return {};
  }

  const language = getBestLanguageForUser(acceptLanguage);
  res.writeHead(302, {
    Location: `/${language}`,
  });
  res.end();
  return {};
};

export default HomeNoLang;
