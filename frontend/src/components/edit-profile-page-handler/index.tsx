/** @jsxRuntime classic */

/** @jsx jsx */
import {
  CardPart,
  Grid,
  Heading,
  Link,
  InputWrapper,
  MultiplePartsCard,
  Page,
  Section,
  Input,
  Text,
  Select,
  Button,
  HorizontalStack,
  Spacer,
  Checkbox,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx, Label } from "theme-ui";
import * as yup from "yup";

import { useRouter } from "next/router";

import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { useCountries } from "~/helpers/use-countries";
import { useMyEditProfileQuery, useUpdateProfileMutation } from "~/types";

import { ErrorsList } from "../errors-list";

type MeUserFields = {
  name: string;
  fullName: string;
  gender: string;
  dateBirth: Date;
  country: string;
  openToRecruiting: boolean;
  openToNewsletter: boolean;
};

const schema = yup.object().shape({
  name: yup.string().required().ensure(),
  fullName: yup.string().required().ensure(),
  gender: yup.string().required().ensure(),
  dateBirth: yup.date(),
  country: yup.string().required().ensure(),
  openToRecruiting: yup.boolean(),
  openToNewsletter: yup.boolean(),
});

const onMyProfileFetched = (data, formState) => {
  const { me } = data;

  formState.setField("name", me.name ? me.name : "");
  formState.setField("fullName", me.fullName ? me.fullName : "");
  formState.setField("gender", me.gender ? me.gender : "");
  formState.setField(
    "dateBirth",
    me.dateBirth ? new Date(me.dateBirth) : new Date(),
  );
  formState.setField("country", me.country ? me.country : "");
  formState.setField(
    "openToRecruiting",
    me.openToRecruiting ? me.openToRecruiting : false,
  );
  formState.setField(
    "openToNewsletter",
    me.openToNewsletter ? me.openToNewsletter : false,
  );
};

const toTileCase = (word: string) =>
  word.charAt(0).toUpperCase() + word.slice(1);

export const EditProfilePageHandler = () => {
  const router = useRouter();
  const [loggedIn] = useLoginState();
  const [formState, { text, select, checkbox, raw }] =
    useFormState<MeUserFields>(
      {},
      {
        withIds: true,
      },
    );

  const {
    data: profileData,
    loading,
    error,
  } = useMyEditProfileQuery({
    skip: !loggedIn,
    onCompleted: (data) => onMyProfileFetched(data, formState),
  });

  const countries = useCountries();

  if (error) {
    throw new Error(`Unable to fetch profile, ${error}`);
  }

  const getValidationError = (
    key:
      | "name"
      | "fullName"
      | "gender"
      | "dateBirth"
      | "country"
      | "openToRecruiting"
      | "openToNewsletter",
  ) => {
    const validationKey = "validation" + toTileCase(key);
    const validationError =
      (updateProfileData &&
        updateProfileData.updateProfile.__typename ===
          "UpdateProfileValidationError" &&
        (updateProfileData.updateProfile as any).errors[validationKey]
          .map((e) => e.message)
          .join(", ")) ||
      "";
    return validationError;
  };

  const [update, { loading: updateProfileLoading, data: updateProfileData }] =
    useUpdateProfileMutation({
      onCompleted: (data) => {
        if (data?.updateProfile?.__typename === "User") {
          router.push("/profile");
        }
      },
    });

  useEffect(() => {
    if (profileData && !loading) {
      onMyProfileFetched(profileData, formState);
    }
  }, []);

  const onFormSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      try {
        await schema.validate(formState.values, { abortEarly: false });

        formState.errors = {};

        update({
          variables: {
            input: {
              name: formState.values.name,
              fullName: formState.values.fullName,
              gender: formState.values.gender,
              dateBirth: formState.values.dateBirth.toISOString().split("T")[0],
              country: formState.values.country,
              openToRecruiting: formState.values.openToRecruiting,
              openToNewsletter: formState.values.openToNewsletter,
            },
          },
        });
      } catch (err) {
        err.inner.forEach((item) => {
          formState.setFieldError(item.path, item.message);
        });
      }
    },
    [update, formState],
  );

  if (loading || !loggedIn) {
    return null;
  }

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.edit.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="pink">
        <Heading size="display2">
          <FormattedMessage id="profile.myProfile" />
        </Heading>
      </Section>

      <Section>
        <form onSubmit={onFormSubmit}>
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
                    errors={[
                      formState.errors?.name || getValidationError("name"),
                    ]}
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
                      formState.errors?.fullName ||
                        getValidationError("fullName"),
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
                      onChange: (
                        event: React.ChangeEvent<HTMLInputElement>,
                      ) => {
                        const timestamp = Date.parse(event.target.value);

                        if (!isNaN(timestamp)) {
                          const date = new Date(timestamp);
                          formState.setField("dateBirth", date);
                          return date;
                        }

                        return formState.values.dateBirth;
                      },
                    })}
                    value={
                      formState.values.dateBirth &&
                      formState.values.dateBirth.toISOString().split("T")[0]
                    }
                    type="date"
                    required={true}
                    errors={[
                      formState.errors?.dateBirth ||
                        getValidationError("dateBirth"),
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
                      formState.errors?.country ||
                        getValidationError("country"),
                    ]}
                  >
                    {countries.map((c) => (
                      <option key={c.value} value={c.value}>
                        {c.label}
                      </option>
                    ))}
                  </Select>
                </InputWrapper>
              </Grid>
            </CardPart>
          </MultiplePartsCard>
          <Spacer size="medium" />

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
          <Spacer size="large" />

          <HorizontalStack
            wrap="wrap"
            alignItems="center"
            gap="medium"
            justifyContent="spaceBetween"
          >
            <div>
              <ErrorsList errors={[]} />
            </div>
            <Button role="secondary" disabled={updateProfileLoading}>
              <FormattedMessage id="buttons.save" />
            </Button>
          </HorizontalStack>
        </form>
      </Section>
    </Page>
  );
};
