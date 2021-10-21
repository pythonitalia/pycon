/** @jsxRuntime classic */

/** @jsx jsx */
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState } from "~/apollo/client";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useMessages } from "~/helpers/use-messages";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useSocialLoginCheckQuery } from "~/types";

export const LoginSuccessPage = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const router = useRouter();
  const { addMessage } = useMessages();

  const errorMessage = useTranslatedMessage("global.somethingWentWrong");
  const { loading, error } = useSocialLoginCheckQuery({
    onCompleted(data) {
      if (data.me) {
        setLoggedIn(true);
        router.replace("/[lang]/profile", `/${language}/profile/`);
      }
    },
  });

  useEffect(() => {
    if (loggedIn) {
      router.replace("/[lang]/profile", `/${language}/profile/`);
    }

    if (!loading && error) {
      addMessage({
        message: errorMessage,
        type: "alert",
      });

      router.push("/[lang]/login", `/${language}/login/`);
    }
  }, [loggedIn, loading, error]);

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 2,
      }}
    >
      {loading && <FormattedMessage id="login.loading" />}
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await prefetchSharedQueries(lang);

  return addApolloState({
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default LoginSuccessPage;
