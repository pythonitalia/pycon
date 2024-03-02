/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Label, jsx } from "theme-ui";

import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";

type Props = {
  children: React.ReactElement;
  languages: string[];
  value: { [string: string]: string };
  onChange: (event: any) => void;
  name: string;
};

export const MultiLingualInput = ({
  children,
  languages: unsortedLanguages,
  value,
  onChange,
  name: originalName,
  ...props
}: Props) => {
  let languages: string[];
  if (unsortedLanguages.length === 0) {
    languages = ["invalid"];
  } else {
    languages = unsortedLanguages.sort((a) => (a === "en" ? -1 : 1));
  }

  return (
    <Grid
      sx={{
        gap: "20px",
      }}
    >
      {languages.map((language) => {
        const isInvalid = language === "invalid";
        const name = `${originalName}-${language}`;
        return (
          <Box>
            <Label
              htmlFor={name}
              sx={{
                display: "flex",
                alignItems: "center",
                mr: 2,
                pb: 2,
                userSelect: "none",
              }}
            >
              {language === "it" && (
                <ItalianIcon
                  sx={{
                    width: 20,
                    flexShrink: 0,
                  }}
                />
              )}
              {language === "en" && (
                <EnglishIcon
                  sx={{
                    width: 20,
                    flexShrink: 0,
                  }}
                />
              )}
              {!isInvalid && (
                <Box
                  sx={{
                    ml: 2,
                    fontWeight: "bold",
                  }}
                  as="span"
                >
                  <FormattedMessage
                    id={`multilingualinput.language.${language}`}
                  />
                </Box>
              )}
            </Label>

            {React.cloneElement(children, {
              value: isInvalid ? "" : value[language],
              disabled: isInvalid,
              id: name,
              name,
              cursor: isInvalid ? "not-allowed" : "",
              onChange: (e: { target: { value: any } }) => {
                onChange({
                  ...value,
                  [language]: e.target.value,
                });
              },
              ...props,
            })}
          </Box>
        );
      })}
    </Grid>
  );
};
