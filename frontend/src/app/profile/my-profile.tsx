/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { InputWrapper } from "../../components/input-wrapper";
import { Link } from "../../components/link";
import { MyProfileQuery } from "../../generated/graphql-backend";

export const MyProfile: React.SFC<{ profile: MyProfileQuery }> = ({
  profile: { me },
}) => {
  const profileView = [
    { label: "profile.email", value: me.email },
    { label: "profile.fullName", value: me.fullName },
    { label: "profile.name", value: me.name },
    {
      label: "profile.gender",
      value: <FormattedMessage id={`profile.gender.${me.gender}`} />,
    },
    { label: "profile.country", value: me.country },
    { label: "profile.dateBirth", value: me.dateBirth },
    {
      label: "profile.openToNewsletter",
      value: me.openToNewsletter ? (
        <FormattedMessage id="global.yes" />
      ) : (
        <FormattedMessage id="global.no" />
      ),
    },
    {
      label: "profile.openToRecruiting",
      value: me.openToRecruiting ? (
        <FormattedMessage id="global.yes" />
      ) : (
        <FormattedMessage id="global.no" />
      ),
    },
  ];

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 4,
          px: 3,
        }}
      >
        <Heading mb={2} as="h2">
          <FormattedMessage id="profile.profileHeader" />
        </Heading>

        <Link href={`/:language/profile/edit/`}>
          <FormattedMessage id="profile.editProfile" />
        </Link>

        {profileView
          .filter(({ value }) => typeof value !== "undefined")
          .map(({ value, label }) => (
            <InputWrapper
              sx={{ mt: 3, mb: 0 }}
              key={label}
              label={<FormattedMessage id={label} />}
            >
              {value}
            </InputWrapper>
          ))}
      </Box>
    </Box>
  );
};
