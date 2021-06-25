/** @jsxImportSource theme-ui */
import React from "react";
import { Box, Text } from "theme-ui";

import { ErrorsList } from "../errors-list";

export const InputWrapper = ({
  label,
  description,
  className,
  errors,
  isRequired,
  children,
  ...props
}: {
  label?: React.ReactElement | string;
  description?: React.ReactElement;
  errors?: string[];
  className?: string;
  isRequired?: boolean;
  as?: any;
  children: React.ReactNode;
}) => (
  <Box mb={4} {...props} className={className}>
    <Text as="label">
      <Text as="div" sx={{ mb: 1 }} variant="label">
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
