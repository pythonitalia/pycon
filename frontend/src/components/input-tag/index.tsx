/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { Badge, Box, Flex } from "@theme-ui/components";
import { useContext } from "react";
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
};

export const InputTag: React.SFC<InputTagProps> = ({ tag, onClick }) => (
  <Badge variant="tag" className="inputTag" onClick={onClick}>
    {tag.name}
  </Badge>
);

type TagLineProps = {
  tags: SubmissionTag[] | undefined;
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
  const submissionTags = data?.submissionTags;

  const selectTagClick = (id: string) => {
    console.log(id);
    const newTag = submissionTags?.filter(tag => tag?.id === id);

    if (newTag?.length === 0) {
      return;
    }

    console.log(newTag);
    const newTags = [...(tags || []), ...newTag];
    onTagChange(newTags);
  };

  const removeTagClick = (id: string) => {
    onTagChange(tags?.filter(tag => tag.id !== id));
  };

  const getAvailableTags = () => {
    const selectedTagIds = tags?.map(item => item.id);
    if (!selectedTagIds) {
      return submissionTags;
    }
    return submissionTags?.filter(
      tag => selectedTagIds?.indexOf(tag.id) === -1,
    );
  };

  return (
    <Flex>
      {!loading && (
        <Flex sx={{ display: "block" }}>
          <Box>
            <Flex>
              {getAvailableTags()?.map(tag => (
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
                height: 50,
                width: "container",
              }}
            >
              <Flex>
                {tags &&
                  tags.map((tag, i) => (
                    <Flex key={i}>
                      <InputTag tag={tag} />
                      {allowChange && (
                        <Badge
                          as="button"
                          variant="remove"
                          onClick={() => {
                            removeTagClick(tag?.id);
                          }}
                        >
                          x
                        </Badge>
                      )}
                    </Flex>
                  ))}
              </Flex>
            </Box>
          )}
        </Flex>
      )}
    </Flex>
  );
};
