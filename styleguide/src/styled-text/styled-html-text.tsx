import React from "react";
import { StyledText } from "./styled-text";

type Props = { text: string; baseTextSize?: 1 | 2 };

export const StyledHTMLText = ({ text, baseTextSize = 1 }: Props) => {
  return (
    <StyledText
      baseTextSize={baseTextSize}
      dangerouslySetInnerHTML={{
        __html: text,
      }}
    />
  );
};
