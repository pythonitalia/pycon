import { Button, Checkbox, Flex, Popover, Text } from "@radix-ui/themes";

type Tag = { id: string; name: string };

type Props = {
  tags: Tag[];
  excluded: string[];
  onChange: (excluded: string[]) => void;
};

export const TagFilter = ({ tags, excluded, onChange }: Props) => {
  const toggle = (tagId: string, hide: boolean) =>
    onChange(
      hide ? [...excluded, tagId] : excluded.filter((id) => id !== tagId),
    );

  return (
    <Popover.Root>
      <Popover.Trigger>
        <Button size="2" variant="soft" color="gray">
          {excluded.length > 0
            ? `Hiding ${excluded.length} ${excluded.length === 1 ? "tag" : "tags"}`
            : "Hide tags"}
        </Button>
      </Popover.Trigger>
      <Popover.Content width="320px" maxHeight="420px">
        <Text as="p" size="2" weight="bold" mb="1">
          Don't show me these tags
        </Text>
        <Text as="p" size="1" color="gray" mb="3">
          Proposals with any of these tags are skipped in your queue.
        </Text>
        <Flex gap="3" mb="3">
          <Button
            size="1"
            variant="soft"
            onClick={() => onChange(tags.map((tag) => tag.id))}
          >
            Select all
          </Button>
          <Button size="1" variant="soft" onClick={() => onChange([])}>
            Deselect all
          </Button>
        </Flex>
        <Flex direction="column" gap="2">
          {tags.map((tag) => (
            <Text as="label" size="2" key={tag.id}>
              <Flex gap="2" align="center">
                <Checkbox
                  checked={excluded.includes(tag.id)}
                  onCheckedChange={(checked) =>
                    toggle(tag.id, checked === true)
                  }
                />
                {tag.name}
              </Flex>
            </Text>
          ))}
        </Flex>
        <Text as="p" size="1" color="gray" mt="3">
          Applies from the next proposal.
        </Text>
      </Popover.Content>
    </Popover.Root>
  );
};
