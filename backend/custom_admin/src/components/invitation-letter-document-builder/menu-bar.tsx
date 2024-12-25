import * as Toolbar from "@radix-ui/react-toolbar";
import clsx from "clsx";
import {
  AlignCenter,
  AlignJustify,
  AlignLeft,
  AlignRight,
  Bold,
  Italic,
} from "lucide-react";

export const MenuBar = ({ editor }) => {
  return (
    <Toolbar.Root className="flex p-2 gap-1 border-b bg-gray-50 rounded-t-md">
      <Toolbar.Button
        onClick={() => editor.chain().focus().toggleBold().run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive("bold"),
        })}
      >
        <Bold size={16} />
      </Toolbar.Button>

      <Toolbar.Button
        onClick={() => editor.chain().focus().toggleItalic().run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive("italic"),
        })}
      >
        <Italic size={16} />
      </Toolbar.Button>

      <Toolbar.Separator className="w-px bg-gray-300 mx-1" />

      <Toolbar.Button
        onClick={() => editor.chain().focus().setTextAlign("left").run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive({ textAlign: "left" }),
        })}
      >
        <AlignLeft size={16} />
      </Toolbar.Button>

      <Toolbar.Button
        onClick={() => editor.chain().focus().setTextAlign("center").run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive({ textAlign: "center" }),
        })}
      >
        <AlignCenter size={16} />
      </Toolbar.Button>

      <Toolbar.Button
        onClick={() => editor.chain().focus().setTextAlign("right").run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive({ textAlign: "right" }),
        })}
      >
        <AlignRight size={16} />
      </Toolbar.Button>

      <Toolbar.Button
        onClick={() => editor.chain().focus().setTextAlign("justify").run()}
        className={clsx("p-2 rounded hover:bg-gray-200", {
          "bg-gray-200": editor.isActive({ textAlign: "justify" }),
        })}
      >
        <AlignJustify size={16} />
      </Toolbar.Button>
    </Toolbar.Root>
  );
};
