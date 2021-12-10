/** @jsxRuntime classic */

/** @jsx jsx */
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useMessages } from "~/helpers/use-messages";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useSocialLoginCheckQuery } from "~/types";

export const LoginSuccessPage = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const router = useRouter();
  const { addMessage } = useMessages();

  const errorMessage = useTranslatedMessage("global.somethingWentWrong");
  const { loading, error } = useSocialLoginCheckQuery({
    onCompleted(data) {
      if (data.me) {
        setLoggedIn(true);
        router.replace("/profile");
      }
    },
  });

  useEffect(() => {
    if (loggedIn) {
      router.replace("/profile");
    }

    if (!loading && error) {
      addMessage({
        message: errorMessage,
        type: "alert",
      });

      router.push("/login");
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

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export default LoginSuccessPage;
