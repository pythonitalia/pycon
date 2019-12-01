/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { Badge, Box, Button, Flex } from "@theme-ui/components";
import { useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import {
  SubmissionTag,
  TagsQuery,
  TagsQueryVariables,
} from "../../generated/graphql-backend";
import TAGS_QUERY from "./tags.graphql";

type InputTagProps = {
  tag: SubmissionTag;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  variant?: "tag" | "selectedTag";
};

export const InputTag: React.SFC<InputTagProps> = ({
  tag,
  onClick,
  variant = "tag",
}) => (
  <Badge variant={variant} onClick={onClick}>
    {tag.name}
  </Badge>
);

type TagLineProps = {
  tags: SubmissionTag[];
  onTagChange?: any;
  allowChange?: boolean;
};

export const TagLine: React.SFC<TagLineProps> = ({
  tags,
  onTagChange,
  allowChange,
}) => {
  const conferenceCode = useContext(ConferenceContext);
  const { loading, error, data } = useQuery<TagsQuery, TagsQueryVariables>(
    TAGS_QUERY,
    {
      variables: {
        conference: conferenceCode,
      },
    },
  );

  if (loading) {
    return null;
  }

  const submissionTags = data!.submissionTags!;

  const selectTagClick = (id: string) => {
    const newTag = submissionTags?.filter(tag => tag?.id === id);

    if (newTag?.length === 0) {
      return;
    }

    const newTags = [...(tags || []), ...newTag];

    onTagChange(newTags);
  };

  const removeTagClick = (id: string) => {
    onTagChange(tags?.filter(tag => tag.id !== id));
  };

  const selectedTagIds = tags.map(item => item.id);
  const availableTags = submissionTags.filter(
    tag => selectedTagIds?.indexOf(tag.id) === -1,
  );

  return (
    <Flex>
      {!loading && (
        <Box>
          <Box>
            <Flex sx={{ flexWrap: "wrap" }}>
              {availableTags.map(tag => (
                <Flex key={tag.id}>
                  <InputTag
                    tag={tag}
                    onClick={() => {
                      if (allowChange) {
                        selectTagClick(tag?.id);
                      }
                    }}
                  />
                </Flex>
              ))}
            </Flex>
          </Box>
          {allowChange && (
            <Box
              sx={{
                border: "primary",
                mx: "auto",
                px: 3,
                maxWidth: "container",
                width: "container",
              }}
            >
              <Flex>
                {tags.length === 0 && (
                  <Badge variant="placeholderTag">
                    <FormattedMessage id="inputTag.selectTags" />
                  </Badge>
                )}
                {tags.map(tag => (
                  <InputTag
                    key={tag.id}
                    tag={tag}
                    variant="selectedTag"
                    onClick={(e: React.FormEvent<HTMLButtonElement>) => {
                      e.preventDefault();

                      removeTagClick(tag.id);
                    }}
                  />
                ))}
              </Flex>
            </Box>
          )}
        </Box>
      )}
    </Flex>
  );
};
