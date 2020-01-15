/** @jsx jsx */
import { Box, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../context/language";
import { AddComment } from "./add-comment";

type CommentProps = {
  id: string;
  text: string;
  created: string;
  author: {
    name: string;
    fullName: string;
  };
};

type Props = {
  submissionId: string;
  comments: CommentProps[] | null;
};

export const Comments: React.SFC<Props> = ({ submissionId, comments }) => (
  <Box
    sx={{
      maxWidth: 600,
    }}
  >
    <Heading as="h2" mb={2}>
      <FormattedMessage id="submission.comments" />
    </Heading>

    {comments!.map(comment => (
      <Comment key={comment.id} {...comment} />
    ))}

    <Heading as="h2" mb={2} mt={4}>
      <FormattedMessage id="submission.addComment" />
    </Heading>

    <AddComment submissionId={submissionId} />
  </Box>
);

const Comment: React.SFC<CommentProps> = ({ author, text, created }) => {
  const language = useCurrentLanguage();
  const date = new Date(created);
  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return (
    <Box
      sx={{
        mt: 3,
      }}
    >
      <FormattedMessage
        id="submission.commentHead"
        values={{
          author: <strong>{author.name}</strong>,
          when: formatter.format(date),
        }}
      />
      <Text
        sx={{
          display: "block",
        }}
      >
        {text}
      </Text>
    </Box>
  );
};
