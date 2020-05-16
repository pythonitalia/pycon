/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { InputWrapper } from "~/components/input-wrapper";
import { Link } from "~/components/link";

type Props = {
  profile: {
    me: {
      email?: string | null;
      fullName?: string | null;
      name?: string | null;
      gender?: string | null;
      country?: string | null;
      dateBirth?: string | null;
      openToNewsletter?: boolean | null;
      openToRecruiting?: boolean | null;
    };
  };
};

export const MyProfile: React.SFC<Props> = ({ profile: { me } }) => {
  const profileView = [
    {
      label: "profile.email",
      value: me.email ? me.email : <FormattedMessage id="profile.notSet" />,
    },
    {
      label: "profile.fullName",
      value: me.fullName ? (
        me.fullName
      ) : (
        <FormattedMessage id="profile.notSet" />
      ),
    },
    {
      label: "profile.name",
      value: me.name ? me.name : <FormattedMessage id="profile.notSet" />,
    },
    {
      label: "profile.gender",
      value: (
        <FormattedMessage
          id={me.gender ? `profile.gender.${me.gender}` : `profile.notSet`}
        />
      ),
    },
    {
      label: "profile.country",
      value: me.country ? me.country : <FormattedMessage id="profile.notSet" />,
    },
    {
      label: "profile.dateBirth",
      value: me.dateBirth ? (
        me.dateBirth
      ) : (
        <FormattedMessage id="profile.notSet" />
      ),
    },
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

        <Link path={`/[lang]/profile/edit/`}>
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
