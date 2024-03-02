import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import "../shared/styles.css";
import { DjangoAdminEditorProvider } from "./django-admin-editor-modal";

type Props = {
  children: React.ReactNode;
};

const client = new ApolloClient({
  uri: (window as any).apolloGraphQLUrl,
  cache: new InMemoryCache(),
});

export const Base = ({ children }: Props) => {
  return (
    <ApolloProvider client={client}>
      <DjangoAdminEditorProvider>
        <DndProvider backend={HTML5Backend}>{children}</DndProvider>
      </DjangoAdminEditorProvider>
    </ApolloProvider>
  );
};
