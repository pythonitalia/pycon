import React from "react";
import { Spacer } from "../spacer";
import { Text } from "../text";

type Props = {
  children: React.ReactNode;
  title?: string | React.ReactNode;
  description?: string | React.ReactNode;
  required?: boolean;
};

export const InputWrapper = ({
  children,
  title,
  description,
  required,
}: Props) => {
  return (
    <label className="block">
      {title && (
        <>
          <Text weight="strong" uppercase color="grey-900" size="label3">
            {title}
            {required ? "*" : ""}
          </Text>
          <Spacer size={description ? "thin" : "small"} />
        </>
      )}
      {description && (
        <>
          <Text color="grey-700" size="label3">
            {description}
          </Text>
          <Spacer size="small" />
        </>
      )}
      {children}
    </label>
  );
};
