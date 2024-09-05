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
      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.name" />
        </Title>
        <Spacer size="xs" />
        <Text>{grant.name}</Text>
      </div>

      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.fullName" />
        </Title>
        <Spacer size="xs" />
        <Text>{grant.fullName}</Text>
      </div>

      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.ageGroup" />
        </Title>
        <Spacer size="xs" />

        <Text>
          <FormattedMessage
            id={`grants.form.fields.ageGroup.values.${grant.ageGroup}`}
          />
        </Text>
      </div>

      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.travellingFrom" />
        </Title>
        <Spacer size="xs" />
        <Text>{getCountryLabel(countries, grant.travellingFrom)}</Text>
      </div>

      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.gender" />
        </Title>
        <Spacer size="xs" />
        <Text>
          <FormattedMessage id={`profile.gender.${grant.gender}`} />
        </Text>
      </div>

      <div>
        <Title>
          <FormattedMessage id="grants.form.fields.occupation" />
        </Title>
        <Spacer size="xs" />
        <Text>
          <FormattedMessage
            id={`grants.form.fields.occupation.values.${grant.occupation}`}
          />
        </Text>
      </div>
    </Grid>
  );
};
