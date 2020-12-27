/** @jsxRuntime classic */
/** @jsx jsx */
import { useCallback, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Select } from "theme-ui";
import useOnClickOutside from "use-onclickoutside";

import { Tag } from "~/components/tag";

type Props = {
  tags: { id: string; name: string }[];
  onChange: (value: string[]) => void;
  value: string[];
  className?: string;
};

export const TagsFilter: React.SFC<Props> = ({
  tags,
  onChange,
  value,
  className,
}) => {
  const containerRef = useRef(null);
  const [open, setOpen] = useState(false);
  const toggleExtendedView = useCallback(() => {
    if (tags.length === 0) {
      return false;
    }

    setOpen((o) => !o);
  }, [tags]);
  const close = useCallback(() => setOpen(false), []);

  useOnClickOutside(containerRef, close);

  return (
    <Box ref={containerRef} className={className}>
      <Box onClick={toggleExtendedView}>
        <Select
          defaultValue="none"
          sx={{
            pointerEvents: "none",
            borderRadius: 0,
            backgroundColor: "keppel",
          }}
        >
          <FormattedMessage
            id="voting.tagsFilter"
            values={{
              numFilters: value.length,
            }}
          >
            {(text) => (
              <option value="none" disabled={true}>
                {text}
              </option>
            )}
          </FormattedMessage>
        </Select>
      </Box>
      {open && (
        <Box
          sx={{
            position: "absolute",
            top: "auto",
            left: 0,
            width: "100%",
            backgroundColor: "keppel",
            borderTop: "primary",
            borderBottom: "primary",
            py: [4, 5],
            listStyle: "none",
            transform: "translateY(-2px)",
            zIndex: 1,
          }}
        >
          <Box
            sx={{
              maxWidth: "container",
              mx: "auto",
              px: 3,
            }}
          >
            {tags.map((tag) => (
              <Tag
                key={tag.id}
                sx={{
                  cursor: "pointer",
                  my: 2,
                  backgroundColor:
                    value.findIndex((t) => tag.id === t) === -1
                      ? "transparent"
                      : "white",
                  "&:hover": {
                    backgroundColor: "white",
                  },
                }}
                tag={tag}
                onClick={() => {
                  const newValue = [...value];
                  const foundIndex = newValue.findIndex((t) => tag.id === t);

                  if (foundIndex !== -1) {
                    newValue.splice(foundIndex, 1);
                  } else {
                    newValue.push(tag.id);
                  }

                  onChange(newValue);
                }}
              />
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
};
