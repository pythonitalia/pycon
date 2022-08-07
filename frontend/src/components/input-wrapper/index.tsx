/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { Box, jsx, Text } from "theme-ui";

import { ErrorsList } from "../errors-list";

export const InputWrapper: React.SFC<{
  label?: React.ReactElement | string;
  description?: React.ReactElement;
  errors?: string[];
  className?: string;
  isRequired?: boolean;
  as?: any;
}> = ({
  label,
  description,
  className,
  errors,
  isRequired,
  children,
  as,
  ...props
}) => (
  <Box mb={4} {...props} className={className}>
    <Text as={as}>
      <Text sx={{ mb: 1 }} variant="label">
        {label}
        {label && isRequired && "*"}

        {description && (
          <Text variant="labelDescription" as="p">
            {description}
          </Text>
        )}
      </Text>
      {children}
    </Text>

    <ErrorsList sx={{ mt: 2 }} errors={errors} />
  </Box>
);
