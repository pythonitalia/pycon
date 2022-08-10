/** @jsxRuntime classic */

/** @jsx jsx */

import React, { useState } from "react";
import { FormattedMessage } from "react-intl";

import { jsx, Box, Flex, Grid } from "theme-ui";
import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";

const SharedLanguageContext = React.createContext(undefined);

export const SharedLanguageProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [currentLanguage, setCurrentLanguage] = useState(undefined);
  return (
    <SharedLanguageContext.Provider
      value={{
        currentLanguage,
        setCurrentLanguage,
      }}
    >
      {children}
    </SharedLanguageContext.Provider>
  );
};

type Props = {
  children: React.ReactElement;
  languages: string[];
  value: { [string: string]: string };
  onChange: (event: any) => void;
};

export const MultiLingualInput = ({
  children,
  languages: unsortedLanguages,
  value,
  onChange,
  ...props
}: Props) => {
  let languages;
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
        return (
          <Box>
            <Flex
              sx={{
                alignItems: "center",
                cursor: "pointer",
                mr: 2,
                pb: 2,
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
            </Flex>

            {React.cloneElement(children, {
              value: isInvalid ? "" : value[language],
              disabled: isInvalid,
              sx: {
                cursor: isInvalid ? "not-allowed" : "",
              },
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
