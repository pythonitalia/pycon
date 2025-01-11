import { useState } from "react";
import { RichEditor } from "../../components/shared/rich-editor";
import { Base } from "../shared/base";
import { HideNode } from "../shared/rich-editor/menu-bar";

export const RichEditorWidget = ({ name, value }) => {
  const [updatedValue, setUpdatedValue] = useState(value);

  return (
    <Base widget>
      <RichEditor
        hide={[HideNode.table]}
        content={value}
        onUpdate={(content) => setUpdatedValue(content)}
      />

      <input type="hidden" name={name} value={updatedValue} />
    </Base>
  );
};
