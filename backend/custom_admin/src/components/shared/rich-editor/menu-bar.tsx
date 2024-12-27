import * as Toolbar from "@radix-ui/react-toolbar";
import { DropdownMenu, Flex } from "@radix-ui/themes";
import type { Editor } from "@tiptap/core";
import type { Level as HeadingLevel } from "@tiptap/extension-heading";
import clsx from "clsx";
import {
  AlignCenter,
  AlignJustify,
  AlignLeft,
  AlignRight,
  Bold,
  Bolt,
  Heading,
  Heading1,
  Heading2,
  Heading3,
  Heading4,
  Heading5,
  Heading6,
  Italic,
  Redo,
  Underline,
  Undo,
} from "lucide-react";
import { LinkToolbarButton } from "./link-toolbar-menu";
import { ToolbarButton } from "./toolbar-button";

export enum HideNode {
  buttonNode = 0,
  link = 1,
}

const HEADING_ICONS = {
  1: Heading1,
  2: Heading2,
  3: Heading3,
  4: Heading4,
  5: Heading5,
  6: Heading6,
};

const ALIGN_ICONS = {
  left: AlignLeft,
  center: AlignCenter,
  right: AlignRight,
  justify: AlignJustify,
};

const ALIGN_TOOLTIPS = {
  left: "Align Left",
  center: "Align Center",
  right: "Align Right",
  justify: "Align Justify",
};

export const MenuBar = ({
  editor,
  hide = [],
}: {
  editor: Editor;
  hide?: HideNode[];
}) => {
  return (
    <Toolbar.Root className="flex flex-wrap p-2 gap-1 border-b bg-gray-50 rounded-t-md">
      <ToolbarButton
        onClick={() => editor.chain().focus().toggleBold().run()}
        isActive={editor.isActive("bold")}
        tooltip="Bold"
      >
        <Bold size={16} />
      </ToolbarButton>

      <ToolbarButton
        onClick={() => editor.chain().focus().toggleItalic().run()}
        isActive={editor.isActive("italic")}
        tooltip="Italic"
      >
        <Italic size={16} />
      </ToolbarButton>

      <ToolbarButton
        onClick={() => editor.chain().focus().toggleUnderline().run()}
        isActive={editor.isActive("underline")}
        tooltip="Underline"
      >
        <Underline size={16} />
      </ToolbarButton>

      <DropdownMenu.Root>
        <DropdownMenu.Trigger>
          <ToolbarButton
            isActive={editor.isActive("heading")}
            tooltip="Headings"
          >
            <Flex align="center" gap="1">
              <Heading size={16} />
              <DropdownMenu.TriggerIcon />
            </Flex>
          </ToolbarButton>
        </DropdownMenu.Trigger>

        <DropdownMenu.Content>
          {[1, 2, 3, 4, 5, 6].map((level: HeadingLevel) => {
            const Icon = HEADING_ICONS[level];
            return (
              <DropdownMenu.Item
                key={level}
                onClick={() =>
                  editor.chain().focus().setHeading({ level }).run()
                }
                className={clsx({
                  "bg-gray-200": editor.isActive("heading", { level }),
                })}
              >
                <Icon size={16} />
                Heading {level}
              </DropdownMenu.Item>
            );
          })}
        </DropdownMenu.Content>
      </DropdownMenu.Root>

      {!hide.includes(HideNode.buttonNode) && (
        <ToolbarButton
          onClick={() => {
            if (editor.isActive("buttonNode")) {
              return;
            }

            setTimeout(() => {
              editor
                .chain()
                .insertContent({
                  type: "buttonNode",
                })
                .focus()
                .run();
            });
          }}
          isActive={editor.isActive("buttonNode")}
          tooltip="Button"
        >
          <Bolt size={16} />
        </ToolbarButton>
      )}

      {!hide.includes(HideNode.link) && <LinkToolbarButton editor={editor} />}

      <Separator />

      {["left", "center", "right", "justify"].map((textAlign) => {
        const Icon = ALIGN_ICONS[textAlign];
        return (
          <ToolbarButton
            key={textAlign}
            onClick={() => editor.chain().focus().setTextAlign(textAlign).run()}
            isActive={editor.isActive({ textAlign: textAlign })}
            tooltip={ALIGN_TOOLTIPS[textAlign]}
          >
            <Icon size={16} />
          </ToolbarButton>
        );
      })}

      <Separator />

      <ToolbarButton
        onClick={() => editor.chain().focus().undo().run()}
        disabled={!editor.can().undo()}
        tooltip="Undo"
      >
        <Undo size={16} />
      </ToolbarButton>

      <ToolbarButton
        onClick={() => editor.chain().focus().redo().run()}
        disabled={!editor.can().redo()}
        tooltip="Redo"
      >
        <Redo size={16} />
      </ToolbarButton>
    </Toolbar.Root>
  );
};

const Separator = () => <Toolbar.Separator className="w-px bg-gray-300 mx-1" />;
