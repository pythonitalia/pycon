/** @jsx jsx */
import { Badge, Flex, Input } from "@theme-ui/components";
import { useEffect, useState } from "react";
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
};

export const TagLine: React.SFC<TagLineProps> = ({ tags, onTagChange }) => {
  const [tagInput, setTagInput] = useState("");
  console.log(
    `in TagLine-main-> tags: ` +
      JSON.stringify(tags) +
      ` tagInput: ${tagInput}`,
  );

  const removeTag = (i: number) => {
    const newTags = [...(tags || [])];
    newTags.splice(i, 1);
    onTagChange(newTags);
  };

  const inputKeyDown = e => {
    const val = e.target.value;
    if (e.key === "Enter" && val) {
      if (tags && tags.find(tag => tag.toLowerCase() === val.toLowerCase())) {
        return;
      }

      console.log(`in inputKeyDown-> tags: ` + JSON.stringify(tags));
      console.log(`in inputKeyDown-> tagInput: ` + tagInput);
      onTagChange([...(tags || []), val]);
      setTagInput("");
    } else if (e.key === "Backspace" && !val) {
      removeTag(tags ? tags.length - 1 : 0);
    }
    // props.onTagChange(tags);
  };

  useEffect(() => {
    console.log(`in useEffect-> tags: ` + JSON.stringify(tags));
    // onTagChange(tags);
  }, [tags]);

  return (
    <Flex>
      {tags &&
        tags.map((tag, i) => (
          <Flex key={i}>
            <InputTag name={tag} />
            <Badge
              as="button"
              variant="remove"
              onClick={() => {
                removeTag(i);
              }}
            >
              x
            </Badge>
          </Flex>
        ))}
      <Flex>
        <Input
          onChange={event => {
            setTagInput(event.target.value);
          }}
          onKeyDown={inputKeyDown}
          value={tagInput}
        />
      </Flex>
    </Flex>
  );
};
