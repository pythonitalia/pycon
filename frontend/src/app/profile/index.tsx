/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import { Box, Text } from "@theme-ui/components";
import { Fragment, useContext, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Alert } from "../../components/alert";
import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  MyProfileQuery,
  MyProfileQueryVariables,
} from "../../generated/graphql-backend";
import { useLoginState } from "./hooks";
import { Logout } from "./logout";
import { MyProfile } from "./my-profile";
import { MySubmissions } from "./my-submissions";
import MY_PROFILE_QUERY from "./profile.graphql";

export const ProfileApp: React.SFC<RouteComponentProps> = () => {
  const [_, setLoginState] = useLoginState();
  const lang = useCurrentLanguage();
  const conferenceCode = useContext(ConferenceContext);

  const { loading, error, data: profileData } = useQuery<
    MyProfileQuery,
    MyProfileQueryVariables
  >(MY_PROFILE_QUERY, {
    variables: {
      conference: conferenceCode,
    },
  });

  useEffect(() => {
    const loginUrl = `/${lang}/login`;

    if (error) {
      setLoginState(false);

      navigate(loginUrl);
    }
  }, [error]);

  if (loading) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Alert variant="info">
            <FormattedMessage id="profile.loading" />
          </Alert>
        )}
      </Box>
    );
  }

  if (error || !profileData) {
    return null;
  }

  return (
    <Fragment>
      <MyProfile profile={profileData} />
      <MySubmissions
        sx={{
          borderTop: "primary",
        }}
      />
      <Logout lang={lang} />
    </Fragment>
  );
};
