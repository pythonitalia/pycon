/** @jsxRuntime classic */

/** @jsx jsx */

import React, { useEffect, useState, useContext } from "react";
import { FormattedMessage } from "react-intl";

import { jsx, Box, Flex } from "theme-ui";
import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";

const SharedLanguageContext = React.createContext(undefined);

export const SharedLanguageProvider = ({
  children,
}: React.PropsWithChildren<void>) => {
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
  const languages = unsortedLanguages.sort((a) => (a === "en" ? -1 : 1));
  const { currentLanguage, setCurrentLanguage } = useContext(
    SharedLanguageContext,
  );
  const isDisabled = typeof currentLanguage === "undefined";

  useEffect(() => {
    if (!currentLanguage || !languages.includes(currentLanguage)) {
      setCurrentLanguage(languages[0]);
    }
  }, [languages]);

  let languageValue;
  if (typeof value === "undefined") {
    languageValue = "";
  } else if (typeof value === "string") {
    languageValue = value;
  } else {
    languageValue = value[currentLanguage];
  }

  return (
    <Box>
      <Flex
        as="ul"
        sx={{
          mb: 2,
          userSelect: "none",
        }}
      >
        {languages.map((language) => (
          <Flex
            onClick={() => setCurrentLanguage(language)}
            as="li"
            sx={{
              alignItems: "center",
              cursor: "pointer",
              mr: 2,
              p: 2,
              bg: currentLanguage === language ? "orange" : "transparent",
              color: currentLanguage === language ? "white" : "black",
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
            <Box
              sx={{
                ml: 2,
                fontWeight: "bold",
              }}
              as="span"
            >
              <FormattedMessage id={`multilingualinput.language.${language}`} />
            </Box>
          </Flex>
        ))}
      </Flex>
      <Box
        sx={{
          position: "relative",
        }}
      >
        {React.cloneElement(children, {
          value: languageValue,
          disabled: isDisabled,
          sx: {
            cursor: isDisabled ? "not-allowed" : "",
          },
          onChange: (e: { target: { value: any } }) => {
            onChange({
              ...value,
              [currentLanguage]: e.target.value,
            });
          },
          ...props,
        })}
      </Box>
    </Box>
  );
};
