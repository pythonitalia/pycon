import type { CSSProperties } from "react";
import { useCallback } from "react";
import { Props, default as ReactSelect } from "react-select";
import { borderRadius, marginLeft } from "styled-system";

import { Alert } from "~/components/alert";
import { useTagsQuery } from "~/types";

type TagLineProps = {
  tags: string[];
  onChange?: (tags: { value: string }[]) => void;
};

export const TagsSelect = ({ tags, onChange }: TagLineProps) => {
  const { loading, error, data } = useTagsQuery();

  if (loading) {
    return null;
  }

  if (error) {
    return <Alert variant="alert">{error.message}</Alert>;
  }

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

  return (
    <ReactSelect
      styles={{
        control: (base: CSSProperties) => ({
          ...base,
          position: "relative",
          border: "none",
          borderBottom: "3px solid #0E1116",
          background: "transparent",
          padding: "0px",
          overflow: "visible",
          borderRadius: 0,

          "> div": {
            overflow: "visible",
          },

          "&:hover": {
            borderColor: "#0E1116",
          },
        }),
        menu: (base: CSSProperties): CSSProperties => ({
          ...base,
          border: "3px solid #0E1116",
          zIndex: 1000,
          borderRadius: 0,
        }),
        valueContainer: (base: CSSProperties): CSSProperties => ({
          ...base,
          padding: "0px",
        }),
        option: (base: CSSProperties, state: { isSelected: boolean }) => ({
          ...base,
          background: state.isSelected ? "#f6f6f6" : "#fff",
          fontFamily: "GeneralSans-Variable",
          fontWeight: "500",
          fontSize: "1rem",
          lineHeight: "1.5rem",
          padding: "1rem",
          color: "#0E1116",

          "&:hover, &:focus": {
            background: "rgba(83,138,212,.2)",
          },
        }),
        container: (base: CSSProperties): CSSProperties => ({
          ...base,
          overflow: "visible",
        }),
        dropdownIndicator: (base: CSSProperties): CSSProperties => ({
          ...base,
          color: "#0E1116",
        }),
        clearIndicator: (base: CSSProperties): CSSProperties => ({
          ...base,
          color: "#0E1116",
        }),
        placeholder: (base: CSSProperties): CSSProperties => ({
          ...base,
          fontWeight: "500",
          fontFamily: "GeneralSans-Variable",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
          color: "#BFBCBC",
        }),
        indicatorSeparator: (base: CSSProperties): CSSProperties => ({
          ...base,
          display: "none",
        }),
        multiValue: (base: CSSProperties): CSSProperties => ({
          ...base,
          position: "relative",
          padding: "0",
          marginRight: "16px",
          background: "none",
          fontFamily: "GeneralSans-Variable",
          fontWeight: "500",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
        }),
        multiValueLabel: (base: CSSProperties): CSSProperties => ({
          ...base,
          padding: "0",
          margin: "0",
          fontFamily: "GeneralSans-Variable",
          fontWeight: "500",
          fontSize: "1.25rem",
          lineHeight: "1.375rem",
          color: "#0E1116",
        }),
        multiValueRemove: (
          base: CSSProperties,
          state: { isFocused: boolean },
        ) => ({
          ...base,
          border: "none",
          cursor: "pointer",
          marginLeft: "5px",
          borderRadius: 0,
          color: state.isFocused ? "#DE350B" : "#0E1116",
          fontFamily: "GeneralSans-Variable",
        }),
      }}
      value={value}
      onChange={(tags) => onChange?.(tags || [])}
      isMulti={true}
      isOptionDisabled={() => value.length >= 5}
      name="tags"
      options={submissionTags}
      placeholder="Add tags"
    />
  );
};
