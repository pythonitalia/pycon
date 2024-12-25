import { RichEditor } from "../../components/shared/rich-editor";
import { Base } from "../shared/base";

export const RichEditorWidget = () => {
  return (
    <Base widget>
      <div>
        <RichEditor
          content="<p>Initial content</p>"
          onUpdate={(content) => console.log(content)}
        />
      </div>
    </Base>
  );
};
