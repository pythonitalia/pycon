import { Box, Dialog, Tooltip } from "@radix-ui/themes";
import { Node, mergeAttributes } from "@tiptap/core";
import { ReactNodeViewRenderer } from "@tiptap/react";
import { NodeViewContent, NodeViewWrapper } from "@tiptap/react";
import clsx from "clsx";
import { Link, TriangleAlert, XIcon } from "lucide-react";
import { InsertLinkDialogContent } from "./insert-link-dialog";

const ButtonClasses = "rich-editor-button";

const Action = ({
  children,
  className,
  tooltip,
  visibleOnHover = false,
  ...props
}) => (
  <Tooltip content={tooltip}>
    <Box
      style={{
        boxShadow: "var(--shadow-3)",
      }}
      className={clsx(
        "rounded-[var(--radius-6)] transition-all absolute text-black bg-white",
        {
          "group-hover/button:opacity-100 opacity-0": visibleOnHover,
        },
        className,
      )}
      p="2"
      {...props}
    >
      {children}
    </Box>
  </Tooltip>
);

const ButtonComponent = (props) => {
  const setLink = (link) => {
    props.updateAttributes({
      href: link,
    });
  };

  const link = props.node.attrs.href;

  return (
    <NodeViewWrapper
      as="a"
      data-type="button"
      className={clsx("relative", ButtonClasses)}
    >
      <Dialog.Root>
        <Dialog.Trigger>
          <Action
            visibleOnHover={!!link}
            data-drag-handle
            tooltip={link ? "Change link" : "No link set"}
            className={clsx(
              "top-0 translate-x-[50%] -translate-y-[50%] right-0",
              {
                "group-[.has-focus]/button:bg-white bg-[var(--yellow-5)]":
                  !link,
              },
            )}
          >
            <Link
              size="16"
              className={clsx("group-[.has-focus]/button:!block", {
                hidden: !link,
              })}
            />

            <TriangleAlert
              size="16"
              className={clsx("group-[.has-focus]/button:hidden", {
                hidden: !!link,
              })}
            />
          </Action>
        </Dialog.Trigger>
        <InsertLinkDialogContent onSubmit={setLink} initialValue={link} />
      </Dialog.Root>

      <Action
        visibleOnHover
        onClick={(_) => props.deleteNode()}
        tooltip="Remove"
        className="top-0 -translate-x-[50%] -translate-y-[50%] left-0 bg-[var(--crimson-5)]"
      >
        <XIcon size="16" />
      </Action>

      <NodeViewContent
        placeholder="Type label..."
        className="text-left before:opacity-40 before:text-white group-[.is-empty]/button:before:!block before:hidden before:h-0 before:opacity-0.5 before:float-left before:content-[attr(placeholder)]"
      />
    </NodeViewWrapper>
  );
};

export const ButtonNode = Node.create({
  name: "buttonNode",
  group: "block",
  content: "inline*",
  selectable: true,
  draggable: true,

  addAttributes() {
    return {
      href: "",
    };
  },

  parseHTML() {
    return [
      {
        tag: 'a[data-type="button"]',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      "a",
      mergeAttributes(
        {
          "data-type": "button",
          class: ButtonClasses,
        },
        HTMLAttributes,
      ),
      0,
    ];
  },

  addNodeView() {
    return ReactNodeViewRenderer(ButtonComponent, {
      className: "group/button",
    });
  },
});
