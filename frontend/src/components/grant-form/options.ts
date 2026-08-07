import { GrantType, Occupation } from "~/types";

export const GENDER_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId: "profile.gender.selectGender",
  },
  {
    disabled: false,
    value: "male",
    messageId: "profile.gender.male",
  },
  {
    disabled: false,
    value: "female",
    messageId: "profile.gender.female",
  },
  {
    disabled: false,
    value: "other",
    messageId: "profile.gender.other",
  },
  {
    disabled: false,
    value: "not_say",
    messageId: "profile.gender.not_say",
  },
];

export const OCCUPATION_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId: "global.selectOption",
  },
  {
    disabled: false,
    value: Occupation.Developer,
    messageId: "grants.form.fields.occupation.values.developer",
  },
  {
    disabled: false,
    value: Occupation.Student,
    messageId: "grants.form.fields.occupation.values.student",
  },
  {
    disabled: false,
    value: Occupation.Researcher,
    messageId: "grants.form.fields.occupation.values.researcher",
  },
  {
    disabled: false,
    value: Occupation.Unemployed,
    messageId: "grants.form.fields.occupation.values.unemployed",
  },
  {
    disabled: false,
    value: Occupation.Other,
    messageId: "grants.form.fields.occupation.values.other",
  },
];

export const GRANT_TYPE_OPTIONS = [
  {
    disabled: false,
    value: GrantType.Diversity,
    messageId: "grants.form.fields.grantType.values.diversity",
  },
  {
    disabled: false,
    value: GrantType.Unemployed,
    messageId: "grants.form.fields.grantType.values.unemployed",
  },
  {
    disabled: false,
    value: GrantType.Speaker,
    messageId: "grants.form.fields.grantType.values.speaker",
  },
];
