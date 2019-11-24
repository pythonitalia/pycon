/** @jsx jsx */
import { Badge, Flex, Input } from "@theme-ui/components";
import { useCallback, useState } from "react";
import { jsx } from "theme-ui";

type InputTagProps = {
  name: string;
};

export const InputTag: React.SFC<InputTagProps> = props => (
  <Badge variant="tag">{props.name}</Badge>
);

type TagLineProps = {
  tags: string[] | undefined;
  onTagChange: any;
  allowRemove: boolean;
};

export const TagLine: React.SFC<TagLineProps> = ({
  tags,
  onTagChange,
  allowRemove,
}) => {
  const [tagInput, setTagInput] = useState("");

  const removeLastTag = () => {
    const lastIndex = tags ? tags.length - 1 : 0;
    const newTags = [...(tags || [])];
    newTags.splice(lastIndex, 1);
    onTagChange(newTags);
  };

  const onTagChanged = useCallback(
    e => {
      const val = e.target.value;
      if (e.key === "Enter" && val) {
        if (tags && tags.find(tag => tag.toLowerCase() === val.toLowerCase())) {
          return;
        }

        onTagChange([...(tags || []), val]);
        setTagInput("");
      } else if (e.key === "Backspace" && !val) {
        removeLastTag();
      }
    },
    [tags, tagInput],
  );

  return (
    <Flex>
      {tags &&
        tags.map((tag, i) => (
          <Flex key={i}>
            <InputTag name={tag} />
            {allowRemove && (
              <Badge as="button" variant="remove" onClick={onTagChanged}>
                x
              </Badge>
            )}
          </Flex>
        ))}
      <Flex>
        <Input
          onChange={e => {
            setTagInput(e.target.value);
          }}
          onKeyDown={onTagChanged}
          value={tagInput}
        />
      </Flex>
    </Flex>
  );
};
