import {
  Checkbox,
  Grid,
  HorizontalStack,
  Input,
  InputWrapper,
  Select,
  Text,
  Textarea,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { type DynamicFormDataFragment, FormQuestionType } from "~/types";

export type DynamicFormAnswer = string | string[] | boolean;
export type DynamicFormAnswers = Record<string, DynamicFormAnswer>;

type Question = DynamicFormDataFragment["questions"][number];

type DynamicFormProps = {
  form: DynamicFormDataFragment;
  answers: DynamicFormAnswers;
  onChange: (answers: DynamicFormAnswers) => void;
  getErrors: (questionId: string) => string[];
};

export const DynamicForm = ({
  form,
  answers,
  onChange,
  getErrors,
}: DynamicFormProps) => {
  const setAnswer = (questionId: string, value: DynamicFormAnswer) =>
    onChange({ ...answers, [questionId]: value });

  return (
    <Grid cols={1}>
      {form.questions.map((question) => (
        <InputWrapper
          key={question.id}
          required={question.required}
          title={question.label}
          description={question.description || undefined}
        >
          <QuestionInput
            question={question}
            value={answers[question.id]}
            onChange={(value) => setAnswer(question.id, value)}
            errors={getErrors(question.id) ?? []}
          />
        </InputWrapper>
      ))}
    </Grid>
  );
};

type QuestionInputProps = {
  question: Question;
  value: DynamicFormAnswer | undefined;
  onChange: (value: DynamicFormAnswer) => void;
  errors: string[];
};

const QuestionInput = ({
  question,
  value,
  onChange,
  errors,
}: QuestionInputProps) => {
  const inputPlaceholderText = useTranslatedMessage("input.placeholder");

  switch (question.questionType) {
    case FormQuestionType.Text:
    case FormQuestionType.Url:
      return (
        <Input
          type={question.questionType === FormQuestionType.Url ? "url" : "text"}
          value={(value as string) ?? ""}
          onChange={(e) => onChange(e.target.value)}
          required={question.required}
          maxLength={question.maxLength ?? undefined}
          placeholder={inputPlaceholderText}
          errors={errors}
        />
      );

    case FormQuestionType.Textarea:
      return (
        <Textarea
          rows={2}
          value={(value as string) ?? ""}
          onChange={(e) => onChange(e.target.value)}
          required={question.required}
          maxLength={question.maxLength ?? undefined}
          placeholder={inputPlaceholderText}
          errors={errors}
        />
      );

    case FormQuestionType.Select:
      return (
        <Select
          value={(value as string) ?? ""}
          onChange={(e) => onChange(e.target.value)}
          required={question.required}
          errors={errors}
        >
          <FormattedMessage id="global.selectOption">
            {(msg) => (
              <option value="" disabled={question.required}>
                {msg}
              </option>
            )}
          </FormattedMessage>
          {question.options.map((option) => (
            <option key={option.id} value={option.id}>
              {option.label}
            </option>
          ))}
        </Select>
      );

    case FormQuestionType.MultiSelect: {
      const selected = Array.isArray(value) ? value : [];
      const toggle = (optionId: string) =>
        onChange(
          selected.includes(optionId)
            ? selected.filter((item) => item !== optionId)
            : [...selected, optionId],
        );

      return (
        <>
          <HorizontalStack wrap="wrap" gap="small">
            {question.options.map((option) => (
              <label key={option.id}>
                <HorizontalStack gap="small" alignItems="center">
                  <Checkbox
                    size="small"
                    checked={selected.includes(option.id)}
                    onChange={() => toggle(option.id)}
                  />
                  <Text size={2}>{option.label}</Text>
                </HorizontalStack>
              </label>
            ))}
          </HorizontalStack>
          <QuestionErrors errors={errors} />
        </>
      );
    }

    case FormQuestionType.Boolean:
      return (
        <>
          <Checkbox
            checked={Boolean(value)}
            onChange={(e) => onChange(e.target.checked)}
          />
          <QuestionErrors errors={errors} />
        </>
      );

    default:
      return null;
  }
};

const QuestionErrors = ({ errors }: { errors: string[] }) => {
  if (!errors.length) {
    return null;
  }
  return (
    <>
      <Text as="p" size="label4" color="error" uppercase>
        {errors.join(", ")}
      </Text>
    </>
  );
};
