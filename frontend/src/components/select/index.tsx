/** @jsx jsx */
import React, { CSSProperties } from "react";
import { default as ReactSelect, Props } from "react-select";
import { jsx } from "theme-ui";

export const Select: React.SFC<Props> = props => (
  <ReactSelect
    styles={{
      control: (base: CSSProperties) => ({
        ...base,
        position: "relative",
        border: "4px solid #000",
        background: "#fff",
        padding: "20px 8px",
        overflow: "visible",

        "> div": {
          overflow: "visible",
        },

        "&:hover": {
          borderColor: "#000",
        },
      }),
      menu: (base: CSSProperties): CSSProperties => ({
        ...base,
        border: "4px solid #000",
      }),
      option: (base: CSSProperties, state: { isSelected: boolean }) => ({
        ...base,
        fontFamily: "aktiv-grotesk-extended,sans-serif",
        background: state.isSelected ? "#f6f6f6" : "#fff",
        "&:hover, &:focus": {
          background: "#f6f6f6",
        },
      }),
      container: (base: CSSProperties): CSSProperties => ({
        ...base,
        overflow: "visible",
      }),
      dropdownIndicator: (base: CSSProperties): CSSProperties => ({
        ...base,
        color: "#000",
      }),
      clearIndicator: (base: CSSProperties): CSSProperties => ({
        ...base,
        color: "#000",
      }),
      multiValueRemove: (
        base: CSSProperties,
        state: { isFocused: boolean },
      ) => ({
        ...base,
        position: "absolute",
        top: "-10px",
        right: "-10px",
        width: "26px",
        height: "26px",
        border: "3px solid #000",
        background: state.isFocused ? "#FFBDAD" : "#ffa500",
        borderRadius: "100%",
        cursor: "pointer",
        color: state.isFocused ? "#DE350B" : "#000",
      }),
      placeholder: (base: CSSProperties): CSSProperties => ({
        ...base,
        fontFamily: "inherit",
        color: "#000",
      }),
      indicatorSeparator: (base: CSSProperties): CSSProperties => ({
        ...base,
        background: "#000",
      }),
      multiValue: (base: CSSProperties): CSSProperties => ({
        ...base,
        position: "relative",
        padding: "8px",
        marginRight: "16px",
        fontWeight: "bold",
        background: "#F17A5D",
        border: "3px solid #000",
      }),
    }}
    {...props}
  />
);
