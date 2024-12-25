import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client";
import { Theme } from "@radix-ui/themes";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import "../shared/styles.css";
import clsx from "clsx";
import { DjangoAdminEditorProvider } from "./django-admin-editor-modal";

type Props = {
  children: React.ReactNode;
  widget?: boolean;
};

const client = new ApolloClient({
  uri: "/admin/graphql",
  cache: new InMemoryCache(),
});

export const Base = ({ children, widget = false }: Props) => {
  return (
    <Theme
      className={clsx({
        "is-widget-theme": widget,
      })}
    >
      <ApolloProvider client={client}>
        <DjangoAdminEditorProvider>
          <DndProvider backend={HTML5Backend}>{children}</DndProvider>
        </DjangoAdminEditorProvider>
      </ApolloProvider>
    </Theme>
  );
};
