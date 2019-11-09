/** @jsx jsx */

import {
  Box,
  Button,
  Flex,
  Grid,
  Input,
  Label,
  Radio,
  Select,
  Text,
  Textarea,
} from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

const InputWrapper: React.SFC<{
  label: string;
  description?: string;
  className?: string;
}> = ({ label, description, className, children }) => (
  <Box mb={4} className={className}>
    <Text variant="cfpLabel" as="p">
      {label}
    </Text>
    {description && (
      <Text variant="cfpLabelDescription" as="p">
        {description}
      </Text>
    )}
    {children}
  </Box>
);

export const CfpForm: React.SFC = () => (
  <Box
    sx={{
      maxWidth: "container",
      mx: "auto",
      px: 2,
    }}
  >
    <Text mb={4} as="h1">
      Your idea
    </Text>
    <Box as="form">
      <Label mb={3} htmlFor="type">
        Choose a format
      </Label>

      <Flex mb={5}>
        <Label
          sx={{
            width: "auto",
            marginRight: 3,
            color: "green",
            fontWeight: "bold",
          }}
        >
          <Radio name="type" /> TALK
        </Label>
        <Label
          sx={{
            width: "auto",
            color: "burntSienna",
            fontWeight: "bold",
          }}
        >
          <Radio name="type" /> TUTORIAL
        </Label>
      </Flex>

      <InputWrapper sx={{ mb: 5 }} label="Title">
        <Input name="title" />
      </InputWrapper>

      <Grid
        sx={{
          mb: 5,
          gridColumnGap: 5,
          gridTemplateColumns: [null, "1fr 1fr"],
        }}
      >
        <Box>
          <InputWrapper
            label="Elevator pitch"
            description="You have 300 characters to sell your idea. This is known as the
            ‘elevator pitch’. Make it as exiting and enticing as possible"
          >
            <Textarea
              sx={{
                resize: "vertical",
                minHeight: 200,
              }}
              name="elevatorPitch"
              rows="6"
            />
          </InputWrapper>
        </Box>
        <Box>
          <InputWrapper
            label="Length"
            description="The length of your talk or workshop"
          >
            <Select name="length">
              <option>30 m + 15 QA</option>
              <option>45 m + 15 QA</option>
            </Select>
          </InputWrapper>

          <InputWrapper
            label="Audience Level"
            description="Who is the best target audience?"
          >
            <Select name="audienceLevel">
              <option>Beginners</option>
              <option>Intermedie</option>
              <option>Advanced</option>
            </Select>
          </InputWrapper>
        </Box>
      </Grid>
      <InputWrapper
        sx={{
          mb: 5,
        }}
        label="Description"
        description="This decription will be seen by reviewers and the audience, if selected. You should make the description as compelling and exiting as possible - remember, you’re selling the idea to the organisers as well as appealling to attendees"
      >
        <Textarea
          sx={{
            resize: "vertical",
            minHeight: 200,
          }}
          name="description"
          rows="6"
        />
      </InputWrapper>

      <InputWrapper
        label="Notes"
        description="Notes will only be seen by reviewers. This is where you should explian things such as technical requirements and why you’re the best person for this idea."
      >
        <Textarea
          sx={{
            resize: "vertical",
            minHeight: 150,
          }}
          name="notes"
          rows="4"
        />
      </InputWrapper>

      <Button>Submit</Button>
    </Box>
  </Box>
);
