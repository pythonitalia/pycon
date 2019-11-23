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

export const TagLine: React.SFC<TagLineProps> = props => {
  console.log(`in TagLine-main-> props: ` + JSON.stringify(props));

  const [tags, setTags] = useState(props.tags ? props.tags : []);
  const [tagInput, setTagInput] = useState("");
  console.log(
    `in TagLine-main-> tags: ` +
      JSON.stringify(tags) +
      ` tagInput: ${tagInput}`,
  );

  const removeTag = (i: number) => {
    const newTags = [...tags];
    newTags.splice(i, 1);
    setTags(newTags);
  };
  const inputKeyDown = e => {
    const val = e.target.value;
    if (e.key === "Enter" && val) {
      if (tags && tags.find(tag => tag.toLowerCase() === val.toLowerCase())) {
        return;
      }
      setTags([...tags, val]);
      console.log(tagInput);
      setTagInput("");
    } else if (e.key === "Backspace" && !val) {
      removeTag(tags.length - 1);
    }
    console.log(`in inputKeyDown-> tags: ` + JSON.stringify(tags));
    // props.onTagChange(tags);
  };

  useEffect(() => {
    console.log(`in useEffect-> tags: ` + JSON.stringify(tags));
    props.onTagChange(tags);
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
