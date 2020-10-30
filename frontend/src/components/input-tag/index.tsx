/** @jsx jsx */

import { useCallback } from "react";
import { jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Select } from "~/components/select";
import { useTagsQuery } from "~/types";

type TagLineProps = {
  tags: string[];
  onTagChange?: (tags: { value: string }[]) => void;
};

export const TagLine: React.SFC<TagLineProps> = ({ tags, onTagChange }) => {
  const onChange = useCallback((newTags) => {
    if (onTagChange) {
      onTagChange(newTags || []);
    }
  }, []);

  const { loading, error, data } = useTagsQuery();

  if (loading) {
    return null;
  }

  if (error) {
    return <Alert variant="alert">{error.message}</Alert>;
  }

  const submissionTags = [...data!.submissionTags]!
    .sort((a, b) => {
      if (a.name < b.name) {
        return -1;
      }

      if (a.name > b.name) {
        return 1;
      }

      return 0;
    })
    .map((t) => ({
      value: t.id,
      label: t.name,
    }));

  const value = tags.map((t) => submissionTags.find((s) => s.value === t)!);

  return (
    <Select
      value={value}
      onChange={onChange}
      isMulti={true}
      name="tags"
      options={submissionTags}
    />
  );
};
