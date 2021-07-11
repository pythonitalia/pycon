/** @jsxRuntime classic */
/** @jsx jsx */

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Card, Checkbox, Input, jsx, Label, Select, Text } from "theme-ui";
import * as yup from "yup";

import { addApolloState } from "~/apollo/client";
import { Button } from "~/components/button/button";
import { InputWrapper } from "~/components/input-wrapper";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCountries } from "~/helpers/use-countries";
import { useCurrentLanguage } from "~/locale/context";
import {
  queryCountries,
  useMyEditProfileQuery,
  useUpdateProfileMutation,
} from "~/types";

type MeUserFields = {
  name: string;
  fullName: string;
  gender: string;
  dateBirth: Date;
  country: string;
  openToRecruiting: boolean;
  openToNewsletter: boolean;
};

const SectionWrapper: React.FC<{
  titleId?: string;
  children: React.ReactNode;
}> = ({ titleId, children }) => (
  <Card>
    <Box mb={5}>
      {titleId && (
        <Text mb={3} as="h3">
          <FormattedMessage id={titleId} />
        </Text>
      )}
      {children}
    </Box>
  </Card>
);

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

export const EditProfilePage: React.FC = () => {
  const router = useRouter();
  const language = useCurrentLanguage();
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
          router.push("/[lang]/profile", `/${language}/profile`);
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

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
      }}
    >
      <FormattedMessage id="profile.edit.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Text mb={4} as="h1">
        <FormattedMessage id="profile.header" />
      </Text>

      {loading && "Loading..."}
      {!loading && (
        <Box as="form" onSubmit={onFormSubmit}>
          <SectionWrapper titleId="profile.edit.personalHeader">
            <InputWrapper
              errors={[formState.errors?.name || getValidationError("name")]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.name">
                  {(msg) => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input {...text("name")} required={true} />
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.fullName || getValidationError("fullName"),
              ]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.fullName">
                  {(msg) => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input {...text("fullName")} required={true} />
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.gender || getValidationError("gender"),
              ]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.gender">
                  {(msg) => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Select {...select("gender")}>
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
                <FormattedMessage id="profile.gender.notSay">
                  {(msg) => (
                    <option key="notSay" value="not_say">
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
              </Select>
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.dateBirth || getValidationError("dateBirth"),
              ]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.dateBirth">
                  {(msg) => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Input
                {...raw({
                  name: "dateBirth",
                  onChange: (event: React.ChangeEvent<HTMLInputElement>) => {
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
              />
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.country || getValidationError("country"),
              ]}
              isRequired={true}
              label={
                <FormattedMessage id="profile.country">
                  {(msg) => <b>{msg}</b>}
                </FormattedMessage>
              }
            >
              <Select
                {...select("country")}
                required={true}
                value={formState.values.country}
              >
                {countries.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </Select>
            </InputWrapper>
          </SectionWrapper>
          <br />
          <SectionWrapper titleId="profile.edit.privacyHeader">
            <InputWrapper
              errors={[
                formState.errors?.openToRecruiting ||
                  getValidationError("openToRecruiting"),
              ]}
            >
              <Label>
                <Checkbox
                  {...checkbox("openToRecruiting")}
                  checked={formState.values.openToRecruiting}
                />
                <FormattedMessage id="profile.openToRecruiting" />
              </Label>
            </InputWrapper>

            <InputWrapper
              errors={[
                formState.errors?.openToNewsletter ||
                  getValidationError("openToNewsletter"),
              ]}
            >
              <Label>
                <Checkbox
                  {...checkbox("openToNewsletter")}
                  checked={formState.values.openToNewsletter}
                />
                <FormattedMessage id="profile.openToNewsletter" />
              </Label>
            </InputWrapper>
          </SectionWrapper>
          <Box>
            <Button type="submit" loading={updateProfileLoading}>
              <FormattedMessage id="buttons.save" />
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await Promise.all([prefetchSharedQueries(lang), queryCountries()]);

  return addApolloState({
    props: {},
    revalidate: 1,
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default EditProfilePage;
