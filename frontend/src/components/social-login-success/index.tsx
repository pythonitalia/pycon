import { Box } from "@theme-ui/components";
import { useRouter } from "next/router";
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";

import { useLoginState } from "~/app/profile/hooks";
import { useCurrentLanguage } from "~/locale/context";
import { useSocialLoginCheckQuery } from "~/types";

export const SocialLoginSuccess: React.SFC = () => {
  const [loggedIn, setLoggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const router = useRouter();

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
  }, [loggedIn]);

  if (!loading && error) {
    // TODO
    // return (
    //   <Redirect
    //     to={`/${lang}/login/`}
    //     state={{
    //       message: "Something went wrong, please try again",
    //     }}
    //     noThrow={true}
    //   />
    // );
  }

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
