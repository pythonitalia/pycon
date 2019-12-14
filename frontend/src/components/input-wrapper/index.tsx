/** @jsx jsx */
import { Box, Label, Text } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

export const InputWrapper: React.SFC<{
  label?: React.ReactElement;
  description?: React.ReactElement;
  errors?: string[];
  className?: string;
  isRequired?: boolean;
}> = ({
  label,
  description,
  className,
  errors,
  isRequired,
  children,
  ...props
}) => (
  <Box mb={4} {...props} className={className}>
    {label && (
      <Text variant="label" as="p">
        {label}
        {isRequired && "*"}
      </Text>
    )}
    {description && (
      <Text variant="labelDescription" as="p">
        {description}
      </Text>
    )}
    {children}
    {errors && (
      <ul
        sx={{
          mt: 2,
          listStyle: "none",
          color: "red",
        }}
      >
        {errors.map(error => (
          <li key={error}>{error}</li>
        ))}
      </ul>
    )}
  </Box>
);
