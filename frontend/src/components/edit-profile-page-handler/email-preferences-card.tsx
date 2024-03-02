import {
  CardPart,
  Checkbox,
  Grid,
  Heading,
  HorizontalStack,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { FormState, Inputs, StateErrors } from "react-use-form-state";

import { MeUserFields } from "./types";

type Props = {
  formState: FormState<MeUserFields, StateErrors<MeUserFields, string>>;
  formOptions: Inputs<MeUserFields>;
};

export const EmailPreferencesCard = ({
  formState,
  formOptions: { checkbox },
}: Props) => {
  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="profile.editProfile.emailPreferences" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Grid cols={1}>
          <label>
            <HorizontalStack
              wrap="wrap"
              gap="small"
              justifyContent="spaceBetween"
            >
              <Text size={2} weight="strong">
                <FormattedMessage id="profile.openToRecruiting" />
              </Text>
              <Checkbox
                {...checkbox("openToRecruiting")}
                checked={formState.values.openToRecruiting}
              />
            </HorizontalStack>
          </label>
          <label>
            <HorizontalStack
              wrap="wrap"
              gap="small"
              justifyContent="spaceBetween"
            >
              <Text size={2} weight="strong">
                <FormattedMessage id="profile.openToNewsletter" />
              </Text>
              <Checkbox
                {...checkbox("openToNewsletter")}
                checked={formState.values.openToNewsletter}
              />
            </HorizontalStack>
          </label>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
