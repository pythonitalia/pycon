import { useContext, useEffect, useReducer } from "react";
import { useInvitationLetterDocumentQuery } from "./invitation-letter-document.generated";
import { useUpdateInvitationLetterDocumentMutation } from "./update-invitation-letter-document.generated";

import { createContext } from "react";

export const LocalStateContext = createContext<{
  localData: any;
  saveChanges: () => void;
  isSaving: boolean;
  addPage: () => void;
  setContent: (pageId: string, content: string) => void;
  removePage: (pageId: string) => void;
  movePageUp: (pageId: string) => void;
  movePageDown: (pageId: string) => void;
}>({
  localData: null,
  saveChanges: () => {},
  isSaving: false,
  addPage: () => {},
  setContent: () => {},
  removePage: () => {},
  movePageUp: () => {},
  movePageDown: () => {},
});

enum ActionType {
  LoadData = "SET_REMOTE_DATA",
  AddPage = "ADD_PAGE",
  SetContent = "SET_CONTENT",
  RemovePage = "REMOVE_PAGE",
  MovePageUp = "MOVE_PAGE_UP",
  MovePageDown = "MOVE_PAGE_DOWN",
}

const reducer = (state, action) => {
  switch (action.type) {
    case ActionType.LoadData: {
      return {
        ...action.payload,
        __typename: undefined,
        pages: action.payload.pages.map((page) => ({
          ...page,
          __typename: undefined,
        })),
      };
    }
    case ActionType.AddPage: {
      return {
        ...state,
        pages: [
          ...state.pages,
          {
            id: crypto.randomUUID(),
            title: `Page ${state.pages.length + 1}`,
            content: "",
          },
        ],
      };
    }
    case ActionType.RemovePage: {
      return {
        ...state,
        pages: state.pages.filter((page) => page.id !== action.payload.pageId),
      };
    }
    case ActionType.SetContent: {
      const { pageId, content } = action.payload;
      if (pageId === "header" || pageId === "footer") {
        return {
          ...state,
          [pageId]: content,
        };
      }

      return {
        ...state,
        pages: state.pages.map((page) =>
          page.id === pageId ? { ...page, content } : page,
        ),
      };
    }
    case ActionType.MovePageUp: {
      const pageIndex = state.pages.findIndex(
        (page) => page.id === action.payload.pageId,
      );
      if (pageIndex === 0) {
        return state;
      }

      const pages = [...state.pages];
      [pages[pageIndex], pages[pageIndex - 1]] = [
        pages[pageIndex - 1],
        pages[pageIndex],
      ];

      return {
        ...state,
        pages,
      };
    }
    case ActionType.MovePageDown: {
      const pageIndexDown = state.pages.findIndex(
        (page) => page.id === action.payload.pageId,
      );

      if (pageIndexDown === state.pages.length - 1) {
        return state;
      }

      const pagesDown = [...state.pages];
      [pagesDown[pageIndexDown], pagesDown[pageIndexDown + 1]] = [
        pagesDown[pageIndexDown + 1],
        pagesDown[pageIndexDown],
      ];

      return {
        ...state,
        pages: pagesDown,
      };
    }
  }
  return state;
};

export const useLocalData = () => {
  return useContext(LocalStateContext);
};

const useLoadRemoteData = () => {
  const documentId = (window as any).documentId;
  const { data: remoteData } = useInvitationLetterDocumentQuery({
    variables: {
      id: documentId,
    },
  });
  return remoteData?.invitationLetterDocument?.dynamicDocument;
};

const useSaveRemoteData = (): [(newData) => void, boolean] => {
  const [updateInvitationLetter, { loading: savingChanges }] =
    useUpdateInvitationLetterDocumentMutation();

  return [
    (newData) => {
      updateInvitationLetter({
        variables: {
          input: {
            id: (window as any).documentId,
            dynamicDocument: newData,
          },
        },
      });
    },
    savingChanges,
  ];
};

export const LocalStateProvider = ({ children }) => {
  const [localData, dispatch] = useReducer(reducer, null);
  const remoteData = useLoadRemoteData();
  const [saveChanges, isSaving] = useSaveRemoteData();

  useEffect(() => {
    if (!remoteData) {
      return;
    }

    dispatch({ type: ActionType.LoadData, payload: remoteData });
  }, [remoteData]);

  return (
    <LocalStateContext.Provider
      value={{
        localData,
        saveChanges: () => {
          saveChanges(localData);
        },
        isSaving,
        addPage: () => {
          dispatch({ type: ActionType.AddPage });
        },
        setContent: (pageId, content) => {
          dispatch({
            type: ActionType.SetContent,
            payload: { pageId, content },
          });
        },
        removePage: (pageId) => {
          dispatch({
            type: ActionType.RemovePage,
            payload: { pageId },
          });
        },
        movePageUp: (pageId) => {
          dispatch({
            type: ActionType.MovePageUp,
            payload: { pageId },
          });
        },
        movePageDown: (pageId) => {
          dispatch({
            type: ActionType.MovePageDown,
            payload: { pageId },
          });
        },
      }}
    >
      {children}
    </LocalStateContext.Provider>
  );
};
