import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import { Grid } from "../grid";
import { Spacer } from "../spacer";

import { Input } from "./input";

export default {
  title: "Input",
  argTypes: {
    placeholder: {
      defaultValue: "Placeholder",
      control: {
        type: "text",
      },
    },
    error: {
      defaultValue: "",
      control: {
        type: "text",
      },
    },
  },
};

export const Primary = ({ placeholder, error }) => {
  return (
    <div className="p-6">
      <Input placeholder={placeholder} errors={[error]} />
    </div>
  );
};

export const PlaceholderAsElement = ({ placeholder, error }) => {
  return (
    <div className="p-6">
      <Input
        placeholder={
          <FormattedMessage id="footer.designedBy" defaultMessage="test" />
        }
        errors={[error]}
      />
    </div>
  );
};

export const MultipleInputs = ({ error }) => {
  const [value, setValue] = useState("");
  return (
    <div className="p-6">
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Placeholder"
      />
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Placeholder 1"
      />
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Placeholder 2"
        maxLength={200}
        errors={[error]}
      />
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Placeholder 3"
      />

      <Spacer size="xl" />

      <Grid cols={3}>
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 3"
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 2"
          maxLength={200}
          errors={[error]}
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 3"
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 3"
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 2"
          errors={[error]}
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 2"
          errors={[error]}
        />
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Placeholder 2"
          errors={[error]}
        />
      </Grid>
    </div>
  );
};
