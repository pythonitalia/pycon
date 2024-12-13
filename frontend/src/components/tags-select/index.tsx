import React, { type ComponentType } from "react";
import {
  type DropdownIndicatorProps,
  type MultiValue,
  default as ReactSelect,
  components,
} from "react-select";

import { ArrowDownIcon } from "@python-italia/pycon-styleguide/icons";
import { useIsClient } from "~/helpers/use-is-client";
import { useTagsQuery } from "~/types";

type TagsSelectProps = {
  tags: string[];
  onChange?: (tags: MultiValue<{ value: string }>) => void;
};

// const BaseDropdownIndicator = components.DropdownIndicator as unknown as ReactNode
const BaseDropdownIndicator = components.DropdownIndicator as ComponentType<
  DropdownIndicatorProps<any, true>
>;

const DropdownIndicator = (props: DropdownIndicatorProps<any, true>) => {
  return (
    <BaseDropdownIndicator {...props}>
      <ArrowDownIcon />
    </BaseDropdownIndicator>
  );
};

export const TagsSelect = ({ tags, onChange }: TagsSelectProps) => {
  const conferenceCode = process.env.conferenceCode;
  const { data } = useTagsQuery({
    variables: {
      conference: conferenceCode,
    },
  });
  const isClient = useIsClient();

  if (!isClient) {
    return null;
  }

  const proposalTags = [...data.conference.proposalTags]
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((t) => ({
      value: t.id,
      label: t.name,
    }));

  const value = tags.map((t) => proposalTags.find((s) => s.value === t));

  return (
    <ReactSelect
      styles={{
        control: (base, state: { isFocused: boolean }) => ({
          ...base,
          position: "relative",
          border: "none",
          borderBottomWidth: "3px",
          borderBottomStyle: "solid",
          borderBottomColor: state.isFocused ? "#9473B0" : "#0E1116",
          background: "transparent",
          padding: "0px",
          overflow: "visible",
          borderRadius: "0px",
          outline: "none",

          "> div": {
            overflow: "visible",
          },

          "&:hover": {
            borderBottomColor: state.isFocused ? "#9473B0" : "#0E1116",
          },
        }),
        menu: (base, state) => ({
          ...base,
          border: "3px solid #0E1116",
          borderRadius: "0px",
          background: "#FAF5F3",
        }),
        valueContainer: (base) => ({
          ...base,
          padding: "0px",
        }),
        option: (base, state: { isFocused: boolean; isDisabled: boolean }) => {
          return {
            ...base,
            background: state.isFocused ? "rgba(83,138,212,.2)" : "#FAF5F3",
            fontFamily: "GeneralSans-Variable",
            fontWeight: "500",
            fontSize: "1rem",
            lineHeight: "1.5rem",
            padding: "1rem",
            color: "#0E1116",
            cursor: state.isDisabled ? "not-allowed" : "pointer",
            opacity: state.isDisabled ? 0.5 : 1,

            "&:active, &:hover, &:focus": {
              background: "rgba(83,138,212,.2)",
            },
          };
        },
        container: (base) => ({
          ...base,
          overflow: "visible",
          "&:focus": {
            borderBottomColor: "#9473B0",
          },
        }),
        dropdownIndicator: (base) => ({
          ...base,
          marginRight: "0.75rem",
          color: "#0E1116",
          padding: "0",
        }),
        clearIndicator: (base) => ({
          ...base,
          color: "#0E1116",
        }),
        placeholder: (base) => ({
          ...base,
          fontWeight: "500",
          fontFamily: "GeneralSans-Variable",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
          color: "#BFBCBC",
        }),
        indicatorSeparator: (base) => ({
          ...base,
          display: "none",
        }),
        multiValue: (base) => ({
          ...base,
          position: "relative",
          padding: "8px",
          marginRight: "4px",
          background: "#79CDE0",
          fontFamily: "GeneralSans-Variable",
          fontWeight: "500",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
        }),
        multiValueLabel: (base) => ({
          ...base,
          padding: "0",
          margin: "0",
          fontFamily: "GeneralSans-Variable",
          fontWeight: "500",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
          color: "#0E1116",
        }),
        multiValueRemove: (base) => ({
          ...base,
          border: "none",
          cursor: "pointer",
          marginLeft: "5px",
          borderRadius: 0,
          color: "#0E1116",
          fontFamily: "GeneralSans-Variable",
          "&:hover": {
            backgroundColor: "#D75353",
            color: "#0E1116",
          },
        }),
      }}
      value={value}
      onChange={(tags) => onChange?.(tags || [])}
      isMulti={true}
      isOptionDisabled={() => value.length >= 3}
      name="tags"
      options={proposalTags}
      placeholder="Add tags"
      components={{ DropdownIndicator }}
    />
  );
};
