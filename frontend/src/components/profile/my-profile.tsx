/** @jsxRuntime classic */
/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, jsx, Text } from "theme-ui";

import { InputWrapper } from "~/components/input-wrapper";
import { Link } from "~/components/link";
import { useCountries } from "~/helpers/use-countries";
import { MyProfileQuery } from "~/types";

export const MyProfile: React.FC<{ profile: MyProfileQuery }> = ({
  profile: { me },
}) => {
  const countries = useCountries();
  const profileView = [
    {
      label: "profile.fullName",
      value: me.fullName ? (
        me.fullName
      ) : (
        <FormattedMessage id="profile.notSet" />
      ),
    },
    {
      label: "profile.country",
      value: me.country ? (
        countries.find((c) => c.value === me.country)?.label
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
      label: "profile.email",
      value: me.email ? me.email : <FormattedMessage id="profile.notSet" />,
    },
    {
      label: "profile.dateBirth",
      value: me.dateBirth ? (
        me.dateBirth
      ) : (
        <FormattedMessage id="profile.notSet" />
      ),
    },
  ];

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 4,
          px: 3,
          gridTemplateColumns: ["1fr", null, "2fr 1fr"],
        }}
      >
        <Box>
          <Heading mb={4} as="h1">
            <FormattedMessage id="profile.profileHeader" />
          </Heading>

          <Link path="/[lang]/profile/edit" variant="button">
            <FormattedMessage id="profile.editProfile" />
          </Link>

          <Grid
            as="ul"
            sx={{
              listStyle: "none",
              gridTemplateColumns: ["1fr", "1fr 1fr"],
              gridColumnGap: [5, 6],
              gridRowGap: [3, 4],
              my: [3, 4],
            }}
          >
            {profileView
              .filter(({ value }) => typeof value !== "undefined")
              .map(({ value, label }) => (
                <InputWrapper
                  as="li"
                  sx={{ mt: 0, mb: 0 }}
                  key={label}
                  label={<FormattedMessage id={label} />}
                >
                  <Text
                    as="span"
                    sx={{
                      wordBreak: "break-word",
                    }}
                  >
                    {value}
                  </Text>
                </InputWrapper>
              ))}
          </Grid>

          <InputWrapper
            sx={{
              mb: [3, 4],
            }}
            label={<FormattedMessage id="profile.openToNewsletter" />}
          >
            {me.openToNewsletter ? (
              <FormattedMessage id="global.yes" />
            ) : (
              <FormattedMessage id="global.no" />
            )}
          </InputWrapper>

          <InputWrapper
            sx={{ mb: 0 }}
            label={<FormattedMessage id="profile.openToRecruiting" />}
          >
            {me.openToRecruiting ? (
              <FormattedMessage id="global.yes" />
            ) : (
              <FormattedMessage id="global.no" />
            )}
          </InputWrapper>
        </Box>

        <Box>{/* implement avatar here soon-ish */}</Box>
      </Grid>
    </Box>
  );
};
