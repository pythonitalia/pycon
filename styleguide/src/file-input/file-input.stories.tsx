import React from "react";
import { FileInput } from "./file-input";

export default {
  title: "File Input",
  argTypes: {
    error: {
      defaultValue: "",
      control: {
        type: "text",
      },
    },
  },
};

export const Primary = ({ error }) => {
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  return (
    <FileInput
      onChange={(file) => setSelectedFile(file)}
      placeholder="Upload your image"
      errors={[error]}
      value={selectedFile}
    />
  );
};
