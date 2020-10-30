/** @jsx jsx */

import { useRouter } from "next/router";
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { useMessages } from "~/helpers/use-messages";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useSocialLoginCheckQuery } from "~/types";

export const SocialLoginSuccess: React.SFC = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const router = useRouter();
  const { addMessage } = useMessages();

  const errorMessage = useTranslatedMessage("global.somethingWentWrong");
  const { loading, error, data } = useSocialLoginCheckQuery({
    onCompleted(data) {
      if (data.me) {
        setLoggedIn(true);
      }
    },
  });

  useEffect(() => {
    if (loggedIn) {
      router.push("/[lang]/profile", `/${language}/profile/`);
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
