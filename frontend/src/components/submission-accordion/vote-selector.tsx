/** @jsx jsx */

import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Label, Radio } from "theme-ui";

import { InputWrapper } from "~/components/input-wrapper";

type Props = {
  className?: string;
  label?: string | React.ReactElement;
  onVote: (vote: number) => void;
  value: number;
};

export const VOTE_VALUES = [
  {
    value: 1,
    textId: "voteSelector.notInterested",
  },
  {
    value: 2,
    textId: "voteSelector.maybe",
  },
  {
    value: 3,
    textId: "voteSelector.wantToSee",
  },
  {
    value: 4,
    textId: "voteSelector.mustSee",
  },
];

export const VoteSelector: React.SFC<Props> = ({
  className,
  onVote,
  value,
}) => (
  <Box
    sx={{
      userSelect: "none",
    }}
    className={className}
  >
    <Heading as="h2" sx={{ mb: 3 }}>
      <FormattedMessage id="voteSelector.whatDoYouThink" />
    </Heading>
    <Box
      as="ul"
      sx={{
        width: "100%",
        listStyle: "none",
        display: [null, "flex"],
      }}
    >
      {VOTE_VALUES.map((option) => (
        <li
          sx={{
            cursor: "pointer",
          }}
          key={option.value}
          onClick={(_) => onVote(option.value)}
        >
          <InputWrapper sx={{ mb: 2, mr: 4, textTransform: "none" }}>
            <Label>
              <Radio readOnly={true} checked={value === option.value} />
              <FormattedMessage id={option.textId} />
            </Label>
          </InputWrapper>
        </li>
      ))}
    </Box>
  </Box>
);
