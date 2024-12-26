import { useState } from "react";
import { RichEditor } from "../../components/shared/rich-editor";
import { Base } from "../shared/base";

export const RichEditorWidget = ({ name, value }) => {
  const [updatedValue, setUpdatedValue] = useState(value);

  return (
    <Base widget>
      <RichEditor
        content={value}
        onUpdate={(content) => setUpdatedValue(content)}
      />

      <input type="hidden" name={name} value={updatedValue} />
    </Base>
  );
};
