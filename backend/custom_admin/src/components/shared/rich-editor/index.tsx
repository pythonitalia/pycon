import { Color } from "@tiptap/extension-color";
import Focus from "@tiptap/extension-focus";
import ListItem from "@tiptap/extension-list-item";
import Placeholder from "@tiptap/extension-placeholder";
import TextAlign from "@tiptap/extension-text-align";
import TextStyle from "@tiptap/extension-text-style";
import Underline from "@tiptap/extension-underline";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import clsx from "clsx";
import { ButtonNode } from "./button-node";
import { CustomLink } from "./custom-link";
import { type HideNode, MenuBar } from "./menu-bar";

const extensions = [
  Color.configure({ types: [TextStyle.name, ListItem.name] }),
  TextStyle.configure({ types: [ListItem.name] }),
  StarterKit.configure({
    bulletList: {
      keepMarks: true,
      keepAttributes: false,
    },
    orderedList: {
      keepMarks: true,
      keepAttributes: false,
    },
  }),
  TextAlign.configure({
    types: ["heading", "paragraph"],
  }),
  Underline,
  ButtonNode,
  CustomLink.configure({
    openOnClick: false,
    autolink: true,
    defaultProtocol: "https",
    protocols: ["http", "https"],
    isAllowedUri: (url, ctx) => {
      return true;
    },
  }),
  Placeholder.configure({
    showOnlyCurrent: false,
    placeholder: "",
  }),
  Focus,
];

export const RichEditor = ({
  content,
  onUpdate,
  className,
  hide,
}: {
  content: string;
  onUpdate: (content: string) => void;
  className?: string;
  hide?: HideNode[];
}) => {
  const editor = useEditor({
    extensions,
    content,
    onUpdate: ({ editor }) => {
      onUpdate(editor.getHTML());
    },
    editorProps: {
      attributes: {
        class: clsx("rich-editor outline-none", className),
      },
    },
  });

  return (
    <div className="border">
      <MenuBar hide={hide} editor={editor} />
      <EditorContent editor={editor} className="prose max-w-none p-4" />
    </div>
  );
};
