import Link from "@tiptap/extension-link";

export const CustomLink = Link.extend({
  parseHTML() {
    return [
      {
        tag: 'a:not([data-type="button"])',
      },
    ];
  },
});
