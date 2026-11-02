import { ListItem } from "@tiptap/extension-list";
import {
  Table,
  TableCell,
  TableHeader,
  TableRow,
} from "@tiptap/extension-table";
import TextAlign from "@tiptap/extension-text-align";
import { Color, TextStyle } from "@tiptap/extension-text-style";
import { Focus, Placeholder } from "@tiptap/extensions";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import clsx from "clsx";
import { ButtonNode } from "./button-node";
import { CustomLink } from "./custom-link";
import { type HideNode, MenuBar } from "./menu-bar";

const extensions = [
  Color.configure({ types: [TextStyle.name, ListItem.name] }),
  TextStyle,
  StarterKit.configure({
    bulletList: {
      keepMarks: true,
      keepAttributes: false,
    },
    orderedList: {
      keepMarks: true,
      keepAttributes: false,
    },
    link: false,
  }),
  TextAlign.configure({
    types: ["heading", "paragraph"],
  }),
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
  Table.configure({
    resizable: true,
  }),
  TableRow,
  TableHeader,
  TableCell,
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
    shouldRerenderOnTransaction: true,
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
    <div className="border rounded-md overflow-hidden bg-white text-gray-900">
      <MenuBar hide={hide} editor={editor} />
      <EditorContent editor={editor} className="prose max-w-none p-4" />
    </div>
  );
};
