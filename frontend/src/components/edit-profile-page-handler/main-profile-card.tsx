import {
  Text,
  Heading,
  Grid,
  MultiplePartsCard,
  CardPart,
  InputWrapper,
  Input,
  Select,
  GridColumn,
  Link,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { FormState, Inputs, StateErrors } from "react-use-form-state";

import { useCountries } from "~/helpers/use-countries";
import { MyEditProfileQuery } from "~/types";

import { MeUserFields } from "./types";

type Props = {
  formState: FormState<MeUserFields, StateErrors<MeUserFields, string>>;
  formOptions: Inputs<MeUserFields>;
  profileData: MyEditProfileQuery;
  getValidationError: (field: keyof MeUserFields) => string | undefined;
};

export const MainProfileCard = ({
  formState,
  profileData,
  formOptions: { text, raw, select },
  getValidationError,
}: Props) => {
  const countries = useCountries();
  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="profile.editProfile.generalInformation" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Grid cols={3}>
          <InputWrapper
            required={true}
            title={<FormattedMessage id="profile.name" />}
          >
            <Input
              errors={[formState.errors?.name || getValidationError("name")]}
              {...text("name")}
              required={true}
            />
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="profile.fullName" />}
          >
            <Input
              {...text("fullName")}
              errors={[
                formState.errors?.fullName || getValidationError("fullName"),
              ]}
              required={true}
            />
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="profile.dateBirth" />}
          >
            <Input
              {...raw({
                name: "dateBirth",
                onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
                  const timestamp = Date.parse(event.target.value);

                  if (!Number.isNaN(timestamp)) {
                    const date = new Date(timestamp);
                    formState.setField("dateBirth", date);
                    return date;
                  }

                  return formState.values.dateBirth;
                },
              })}
              value={formState.values.dateBirth?.toISOString().split("T")[0]}
              type="date"
              required={true}
              errors={[
                formState.errors?.dateBirth || getValidationError("dateBirth"),
              ]}
            />
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="profile.gender" />}
          >
            <Select
              errors={[
                formState.errors?.gender || getValidationError("gender"),
              ]}
              {...select("gender")}
            >
              <FormattedMessage id="profile.gender.selectGender">
                {(msg) => <option value="">{msg}</option>}
              </FormattedMessage>
              <FormattedMessage id="profile.gender.male">
                {(msg) => (
                  <option key="male" value="male">
                    {msg}
                  </option>
                )}
              </FormattedMessage>
              <FormattedMessage id="profile.gender.female">
                {(msg) => (
                  <option key="female" value="female">
                    {msg}
                  </option>
                )}
              </FormattedMessage>
              <FormattedMessage id="profile.gender.other">
                {(msg) => (
                  <option key="other" value="other">
                    {msg}
                  </option>
                )}
              </FormattedMessage>
              <FormattedMessage id="profile.gender.not_say">
                {(msg) => (
                  <option key="notSay" value="not_say">
                    {msg}
                  </option>
                )}
              </FormattedMessage>
            </Select>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={
              <FormattedMessage id="profile.country">
                {(msg) => <b>{msg}</b>}
              </FormattedMessage>
            }
          >
            <Select
              {...select("country")}
              required={true}
              value={formState.values.country}
              errors={[
                formState.errors?.country || getValidationError("country"),
              ]}
            >
              {countries.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </Select>
          </InputWrapper>

          <GridColumn colSpan={3}>
            <Text size={2}>
              <FormattedMessage
                id="profile.editProfile.emailInfo"
                values={{
                  email: (
                    <Text size={2} weight="strong">
                      {profileData?.me?.email}
                    </Text>
                  ),
                  contact: (
                    <Link
                      target="_blank"
                      rel="noreferrer noopener"
                      href="mailto:help@pycon.it"
                    >
                      <Text
                        decoration="underline"
                        size={2}
                        weight="strong"
                        color="none"
                      >
                        help@pycon.it
                      </Text>
                    </Link>
                  ),
                }}
              />
            </Text>
          </GridColumn>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
