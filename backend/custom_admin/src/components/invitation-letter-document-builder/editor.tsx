import { Color } from "@tiptap/extension-color";
import ListItem from "@tiptap/extension-list-item";
import TextAlign from "@tiptap/extension-text-align";
import TextStyle from "@tiptap/extension-text-style";
import { EditorContent, useEditor } from "@tiptap/react";
import { useCurrentEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import React from "react";
import { MenuBar } from "./menu-bar";

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
];

export const Editor = ({
  content,
  onUpdate,
}: {
  content: string;
  onUpdate: (content: string) => void;
}) => {
  const editor = useEditor({
    extensions,
    content,
    onUpdate: ({ editor }) => {
      onUpdate(editor.getHTML());
    },
    editorProps: {
      attributes: {
        class: "outline-none",
      },
    },
  });

  return (
    <div className="border rounded-md">
      <MenuBar editor={editor} />
      <EditorContent editor={editor} className="prose max-w-none p-4" />
    </div>
  );
};
