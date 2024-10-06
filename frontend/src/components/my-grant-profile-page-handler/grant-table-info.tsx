import { Grid, Spacer, Text } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import type { MyProfileWithGrantQuery } from "~/types";

import { Title } from "~/components/title";
import { getCountryLabel } from "~/helpers/country-utils";
import { useCountries } from "~/helpers/use-countries";

type Props = {
  grant: MyProfileWithGrantQuery["me"]["grant"];
};

export const GrantTableInfo = ({ grant }: Props) => {
  const countries = useCountries();

  return (
    <Grid cols={3} gap="small" fullWidth>
      <GrantInfo label={<FormattedMessage id="grants.form.fields.name" />}>
        {grant.name}
      </GrantInfo>

      <GrantInfo label={<FormattedMessage id="grants.form.fields.fullName" />}>
        {grant.fullName}
      </GrantInfo>

      <GrantInfo label={<FormattedMessage id="grants.form.fields.ageGroup" />}>
        {grant.ageGroup && (
          <FormattedMessage
            id={`grants.form.fields.ageGroup.values.${grant.ageGroup}`}
          />
        )}
      </GrantInfo>

      <GrantInfo
        label={<FormattedMessage id="grants.form.fields.travellingFrom" />}
      >
        {getCountryLabel(countries, grant.travellingFrom)}
      </GrantInfo>

      <GrantInfo label={<FormattedMessage id="grants.form.fields.gender" />}>
        <FormattedMessage id={`profile.gender.${grant.gender}`} />
      </GrantInfo>

      <GrantInfo
        label={<FormattedMessage id="grants.form.fields.occupation" />}
      >
        <FormattedMessage
          id={`grants.form.fields.occupation.values.${grant.occupation}`}
        />
      </GrantInfo>
    </Grid>
  );
};

const GrantInfo = ({
  label,
  children,
}: {
  label: React.ReactNode;
  children: React.ReactNode;
}) => {
  return (
    <div>
      <Title>{label}</Title>
      <Spacer size="xs" />
      <Text>{children}</Text>
    </div>
  );
};
