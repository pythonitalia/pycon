import React from "react";
import {
  type DropdownIndicatorProps,
  type MultiValue,
  default as ReactSelect,
  components,
} from "react-select";

import { Alert } from "~/components/alert";
import { useIsClient } from "~/helpers/use-is-client";
import { useTagsQuery } from "~/types";

type TagsSelectProps = {
  tags: string[];
  onChange?: (tags: MultiValue<{ value: string }>) => void;
};

const DropdownIndicator = (props: DropdownIndicatorProps<any, true>) => {
  return (
    <components.DropdownIndicator {...props}>
      <svg
        width={20}
        height={12}
        fill="none"
        viewBox="0 0 20 12"
        role="presentation"
        aria-label="Dropdown indicator"
      >
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="M19.878 2.16l-9 9-.707.707-.707-.707-9-9L1.878.746l8.293 8.293L18.464.746l1.414 1.414z"
          fill="#0E1116"
        />
      </svg>
    </components.DropdownIndicator>
  );
};

export const TagsSelect = ({ tags, onChange }: TagsSelectProps) => {
  const { data } = useTagsQuery();
  const isClient = useIsClient();

  const submissionTags = [...data!.submissionTags]!
    .sort((a, b) => {
      if (a.name < b.name) {
        return -1;
      }

      if (a.name > b.name) {
        return 1;
      }

      return 0;
    })
    .map((t) => ({
      value: t.id,
      label: t.name,
    }));

  const value = tags.map((t) => submissionTags.find((s) => s.value === t)!);

  if (!isClient) {
    return null;
  }

  return (
    <ReactSelect
      styles={{
        control: (base) => ({
          ...base,
          position: "relative",
          border: "none",
          borderBottom: "3px solid #0E1116",
          background: "transparent",
          padding: "0px",
          overflow: "visible",
          borderRadius: "0px",

          "> div": {
            overflow: "visible",
          },

          "&:hover": {
            borderColor: "#0E1116",
          },
        }),
        menu: (base) => ({
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
      isOptionDisabled={() => value.length >= 5}
      name="tags"
      options={submissionTags}
      placeholder="Add tags"
      components={{ DropdownIndicator }}
    />
  );
};
