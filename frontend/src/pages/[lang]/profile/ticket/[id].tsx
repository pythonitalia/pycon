/** @jsxRuntime classic */
/** @jsx jsx */
import { useRouter } from "next/router";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Button, Heading, Input, jsx, Select } from "theme-ui";

import { Alert } from "~/components/alert";
import { InputWrapper } from "~/components/input-wrapper";
import { Link } from "~/components/link";
import { useCurrentLanguage } from "~/locale/context";
import { UserTicketInfoQuery, useUserTicketInfoQuery } from "~/types";

type Props = {
  className?: string;
};

type Form = {
  attendeeName: string;
  answers: {
    [id: string]: {
      questionId: string;
      answer: string;
    };
  };
};

export const ManageTicket: React.FC<Props> = () => {
  const { query } = useRouter();
  const lang = useCurrentLanguage();
  const [formState, { text }] = useFormState<Form>({
    answers: {},
  });
  const id = query.id as string;

  const { loading, error, data } = useUserTicketInfoQuery({
    variables: {
      conference: process.env.conferenceCode,
      language: lang,
      id,
    },
    onCompleted(loadedData) {
      const loadedTicket = loadedData?.me.ticket;

      formState.setField("attendeeName", loadedTicket?.attendeeName ?? "");

      formState.setField(
        "answers",
        loadedTicket?.answers.reduce((allAnswers: Form["answers"], answer) => {
          allAnswers[answer.questionId] = {
            questionId: answer.questionId,
            answer: answer.answer ?? "",
          };
          return allAnswers;
        }, {}) ?? {},
      );
    },
  });

  const ticketData = data?.conference.tickets.find(
    (ticket) => ticket.id === data.me.ticket?.itemId,
  )!;

  const onChangeAnswer = (
    e: React.ChangeEvent<HTMLInputElement>,
    question: UserTicketInfoQuery["conference"]["tickets"][0]["questions"][0],
  ) => {
    formState.setField("answers", {
      ...formState.values.answers,
      [question.id]: {
        questionId: question.id,
        answer: e.target.value,
      },
    });
  };

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 4,
          px: 3,
        }}
      >
        <Heading as="h1" mb={4}>
          <FormattedMessage
            id="manageTicket.heading"
            values={{
              ticketName: data?.me.ticket?.ticketName,
            }}
          />
        </Heading>

        {loading && (
          <Alert variant="info">
            <FormattedMessage id="global.loading" />
          </Alert>
        )}

        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Box as="form">
            <InputWrapper label="Attendee name">
              <Input {...text("attendeeName")} required={true} />
            </InputWrapper>

            {ticketData.questions.map((question) => (
              <InputWrapper key={question.id} label={question.name}>
                {question.options.length === 0 && (
                  <Input
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      onChangeAnswer(e, question)
                    }
                    required={question.required}
                    value={formState.values.answers[question.id]?.answer ?? ""}
                  />
                )}
                {question.options.length > 0 && (
                  <Select
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      onChangeAnswer(e, question)
                    }
                    required={question.required}
                    value={formState.values.answers[question.id]?.answer ?? ""}
                  >
                    <FormattedMessage id="manageTicket.notAnswered">
                      {(copy) => <option value="">{copy}</option>}
                    </FormattedMessage>

                    {question.options.map((option) => (
                      <option value={option.id} key={option.id}>
                        {option.name}
                      </option>
                    ))}
                  </Select>
                )}
              </InputWrapper>
            ))}

            <Box>
              <Button>
                <FormattedMessage id="manageTicket.save" />
              </Button>
              <Link
                sx={{
                  display: ["block", "inline-block", null, null],
                  ml: [0, 3],
                  mt: [3, 0],
                }}
                path="/[lang]/profile"
              >
                <FormattedMessage id="manageTicket.goBack" />
              </Link>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default ManageTicket;
