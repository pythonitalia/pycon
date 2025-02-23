import {
  CardPart,
  Grid,
  Heading,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useTranslatedMessage } from "~/helpers/use-translated-message";

export const CoSpeakersSection = () => {
  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="cfp.cospeakers.title" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Text size={2}>
          <FormattedMessage id="cfp.cospeakers.description" />
        </Text>
        <Spacer size="small" />

        <InputWrapper
          required={true}
          title={<FormattedMessage id="cfp.cospeakers.email.title" />}
          description={
            <FormattedMessage id="cfp.cospeakers.email.description" />
          }
        >
          <Input type="email" placeholder={inputPlaceholder} />
        </InputWrapper>
      </CardPart>
    </MultiplePartsCard>
  );
};
