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
    value: "developer",
    messageId: "grants.form.fields.occupation.values.developer",
  },
  {
    disabled: false,
    value: "student",
    messageId: "grants.form.fields.occupation.values.student",
  },
  {
    disabled: false,
    value: "researcher",
    messageId: "grants.form.fields.occupation.values.researcher",
  },
  {
    disabled: false,
    value: "unemployed",
    messageId: "grants.form.fields.occupation.values.unemployed",
  },
  {
    disabled: false,
    value: "other",
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
    value: "diversity",
    messageId: "grants.form.fields.grantType.values.diversity",
  },
  {
    disabled: false,
    value: "unemployed",
    messageId: "grants.form.fields.grantType.values.unemployed",
  },
  {
    disabled: false,
    value: "speaker",
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
    value: "no",
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.no",
  },
  {
    value: "yes",
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.yes",
  },
  {
    value: "absolutely",
    disabled: false,
    messageId: "grants.form.fields.interestedInVolunteering.values.absolutely",
  },
];

export const AGE_GROUPS_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId: "grants.form.fields.ageGroup.values.selectOption",
  },
  {
    value: "range_less_than_10",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_less_than_10",
    isAgeInRange: (age: number) => age <= 10,
  },
  {
    value: "range_11_18",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_11_18",
    isAgeInRange: (age: number) => 11 <= age && age <= 18,
  },
  {
    value: "range_19_24",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_19_24",
    isAgeInRange: (age: number) => 19 <= age && age <= 24,
  },
  {
    value: "range_25_34",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_25_34",
    isAgeInRange: (age: number) => 25 <= age && age <= 34,
  },
  {
    value: "range_35_44",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_35_44",
    isAgeInRange: (age: number) => 35 <= age && age <= 44,
  },
  {
    value: "range_45_54",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_45_54",
    isAgeInRange: (age: number) => 45 <= age && age <= 54,
  },
  {
    value: "range_55_64",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_55_64",
    isAgeInRange: (age: number) => 55 <= age && age <= 64,
  },
  {
    value: "range_more_than_65",
    disabled: false,
    messageId: "grants.form.fields.ageGroup.values.range_more_than_65",
    isAgeInRange: (age: number) => age >= 65,
  },
];
