import {
  AgeGroup,
  GrantType,
  InterestedInVolunteering,
  Occupation,
} from "~/types";

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
    messageId: "grants.form.fields.occupation.values.selectOption",
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
    value: "",
    disabled: true,
    messageId: "grants.form.fields.grantType.values.selectOption",
  },
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

export const INTERESTED_IN_VOLUNTEERING_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId:
      "grants.form.fields.interestedInVolunteering.values.selectOption",
  },
  {
    value: InterestedInVolunteering.No,
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.no",
  },
  {
    value: InterestedInVolunteering.Yes,
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.yes",
  },
  {
    value: InterestedInVolunteering.Absolutely,
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.absolutely",
  },
];

export const AGE_GROUPS_OPTIONS = [
  {
    value: "" as AgeGroup,
    disabled: true,
    messageId: "grants.form.fields.ageGroup.values.selectOption",
  },
  {
    value: AgeGroup.RangeLessThan_10,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_less_than_10",
    isAgeInRange: (age: number) => age <= 10,
  },
  {
    value: AgeGroup.Range_11_18,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_11_18",
    isAgeInRange: (age: number) => 11 <= age && age <= 18,
  },
  {
    value: AgeGroup.Range_19_24,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_19_24",
    isAgeInRange: (age: number) => 19 <= age && age <= 24,
  },
  {
    value: AgeGroup.Range_25_34,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_25_34",
    isAgeInRange: (age: number) => 25 <= age && age <= 34,
  },
  {
    value: AgeGroup.Range_35_44,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_35_44",
    isAgeInRange: (age: number) => 35 <= age && age <= 44,
  },
  {
    value: AgeGroup.Range_45_54,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_45_54",
    isAgeInRange: (age: number) => 45 <= age && age <= 54,
  },
  {
    value: AgeGroup.Range_55_64,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_55_64",
    isAgeInRange: (age: number) => 55 <= age && age <= 64,
  },
  {
    value: AgeGroup.RangeMoreThan_65,
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_more_than_65",
    isAgeInRange: (age: number) => age >= 65,
  },
];
