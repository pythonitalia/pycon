import { Dialog } from "@radix-ui/themes";
import { Link, Unlink } from "lucide-react";
import { InsertLinkDialogContent } from "./insert-link-dialog";
import { ToolbarButton } from "./toolbar-button";

export const LinkToolbarButton = ({ editor }) => {
  const onSubmit = (link) => {
    if (!link) {
      editor.chain().focus().extendMarkRange("link").unsetLink().run();
      return;
    }

    editor
      .chain()
      .focus()
      .extendMarkRange("link")
      .setLink({ href: link })
      .run();
  };

  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <ToolbarButton isActive={editor.isActive("link")} tooltip="Link">
          <Link size={16} />
        </ToolbarButton>
      </Dialog.Trigger>

      <ToolbarButton
        onClick={() => editor.chain().focus().unsetLink().run()}
        disabled={!editor.isActive("link")}
        tooltip="Unlink"
      >
        <Unlink size={16} />
      </ToolbarButton>

      <InsertLinkDialogContent
        onSubmit={onSubmit}
        initialValue={editor.getAttributes("link").href}
      />
    </Dialog.Root>
  );
};
