import { Grid, Text } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";
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
    <Grid cols={1} gap="medium">
      {languages.map((language) => {
        const isInvalid = language === "invalid";
        const name = `${originalName}-${language}`;
        return (
          <div>
            <label htmlFor={name}>
              <div className="flex items-center select-none mr-2 pb-2">
                {language === "it" && (
                  <ItalianIcon className="w-[20px] shrink-0" />
                )}
                {language === "en" && (
                  <EnglishIcon className="w-[20px] shrink-0" />
                )}
                {!isInvalid && (
                  <Text size={2} weight="strong" className="ml-2" as="span">
                    <FormattedMessage
                      id={`multilingualinput.language.${language}`}
                    />
                  </Text>
                )}
              </div>
            </label>

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
          </div>
        );
      })}
    </Grid>
  );
};
