import {
  CardPart,
  Checkbox,
  Grid,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Select,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { MultiLingualInput } from "../multilingual-input";
import { TagsSelect } from "../tags-select";

export const ProposalSection = ({
  conferenceData,
  formOptions,
  getErrors,
  formState,
  allowedDurations,
}) => {
  const inputPlaceholder = useTranslatedMessage("input.placeholder");
  const { radio, raw, select, textarea, checkbox } = formOptions;
  const selectedType = conferenceData!.conference.submissionTypes.find(
    (type) => type.id === formState.values.type,
  );
  const isRecordable = selectedType?.isRecordable;

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="cfp.youridea" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Grid cols={1} gap="medium">
          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.choosetype" />}
            description={<FormattedMessage id="cfp.choosetypeDescription" />}
          >
            <VerticalStack gap="small">
              {conferenceData!.conference.submissionTypes.map((type) => (
                <label key={type.id}>
                  <HorizontalStack gap="small" alignItems="center">
                    <Checkbox
                      {...radio("type", type.id)}
                      required={true}
                      size="small"
                    />
                    <Text weight="strong" size={2}>
                      {type.name}
                    </Text>
                  </HorizontalStack>
                </label>
              ))}
            </VerticalStack>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.languagesLabel" />}
            description={<FormattedMessage id="cfp.languagesDescription" />}
          >
            <HorizontalStack gap="small">
              {conferenceData!.conference.languages.map((language) => (
                <label key={language.code}>
                  <HorizontalStack gap="small" alignItems="center">
                    <Checkbox
                      size="small"
                      {...checkbox("languages", language.code)}
                    />
                    <Text weight="strong" size={2}>
                      {language.name}
                    </Text>
                  </HorizontalStack>
                </label>
              ))}
            </HorizontalStack>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.title" />}
            description={<FormattedMessage id="cfp.titleDescription" />}
          >
            <MultiLingualInput
              {...raw("title")}
              languages={formState.values.languages}
            >
              <Input
                required={true}
                maxLength={100}
                errors={getErrors("validationTitle")}
                placeholder={inputPlaceholder}
              />
            </MultiLingualInput>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.elevatorPitchLabel" />}
            description={<FormattedMessage id="cfp.elevatorPitchDescription" />}
          >
            <MultiLingualInput
              {...raw("elevatorPitch")}
              languages={formState.values.languages}
            >
              <Textarea
                required={true}
                maxLength={300}
                rows={6}
                errors={getErrors("validationElevatorPitch")}
                placeholder={inputPlaceholder}
              />
            </MultiLingualInput>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.lengthLabel" />}
            description={<FormattedMessage id="cfp.lengthDescription" />}
          >
            <Select
              {...select("length")}
              required={true}
              errors={getErrors("validationDuration")}
            >
              <FormattedMessage id="cfp.selectDuration">
                {(txt) => (
                  <option value="" disabled={true}>
                    {txt}
                  </option>
                )}
              </FormattedMessage>
              {allowedDurations!.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </Select>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.audienceLevelLabel" />}
            description={<FormattedMessage id="cfp.audienceLevelDescription" />}
          >
            <Select
              {...select("audienceLevel")}
              required={true}
              errors={getErrors("validationAudienceLevel")}
            >
              <FormattedMessage id="cfp.selectAudience">
                {(txt) => (
                  <option value="" disabled={true}>
                    {txt}
                  </option>
                )}
              </FormattedMessage>
              {conferenceData!.conference.audienceLevels.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </Select>
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.tagsLabel" />}
            description={<FormattedMessage id="cfp.tagsDescription" />}
          >
            <TagsSelect
              tags={formState.values.tags || []}
              onChange={(tags: { value: string }[]) => {
                formState.setField(
                  "tags",
                  tags.map((t) => t.value),
                );
              }}
            />
          </InputWrapper>

          <InputWrapper
            required={true}
            title={<FormattedMessage id="cfp.abstractLabel" />}
            description={<FormattedMessage id="cfp.abstractDescription" />}
          >
            <MultiLingualInput
              {...raw("abstract")}
              languages={formState.values.languages}
            >
              <Textarea
                required={true}
                maxLength={5000}
                rows={6}
                errors={getErrors("validationAbstract")}
                placeholder={inputPlaceholder}
              />
            </MultiLingualInput>
          </InputWrapper>

          <InputWrapper
            title={<FormattedMessage id="cfp.notesLabel" />}
            description={<FormattedMessage id="cfp.notesDescription" />}
          >
            <Textarea
              {...textarea("notes")}
              maxLength={1000}
              rows={4}
              errors={getErrors("validationNotes")}
              placeholder={inputPlaceholder}
            />
          </InputWrapper>

          <InputWrapper
            required={false}
            title={<FormattedMessage id="cfp.shortSocialSummaryLabel" />}
            description={
              <FormattedMessage id="cfp.shortSocialSummaryDescription" />
            }
          >
            <Textarea
              {...textarea("shortSocialSummary")}
              required={false}
              maxLength={128}
              rows={2}
              errors={getErrors("validationShortSocialSummary")}
              placeholder={inputPlaceholder}
            />
          </InputWrapper>

          {isRecordable && (
            <InputWrapper
              required={false}
              title={<FormattedMessage id="cfp.doNotRecordLabel" />}
              description={<FormattedMessage id="cfp.doNotRecordDescription" />}
            >
              <label>
                <HorizontalStack gap="small" alignItems="center">
                  <Checkbox
                    {...checkbox("doNotRecord")}
                    required={false}
                    errors={getErrors("validationDoNotRecord")}
                  />
                  <Text size={2} weight="strong">
                    <FormattedMessage id="cfp.doNotRecordCheckboxLabel" />
                  </Text>
                </HorizontalStack>
              </label>
            </InputWrapper>
          )}
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
