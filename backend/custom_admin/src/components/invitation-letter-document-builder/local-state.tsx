import equal from "fast-deep-equal";
import { useContext, useEffect, useMemo, useReducer } from "react";
import { useInvitationLetterDocumentSuspenseQuery } from "./invitation-letter-document.generated";
import { useUpdateInvitationLetterDocumentMutation } from "./update-invitation-letter-document.generated";

import { createContext } from "react";
import { useArgs } from "../shared/args";

type State = {
  header: string;
  footer: string;
  pages: {
    id: string;
    title: string;
    content: string;
  }[];
};

export const LocalStateContext = createContext<{
  localData: State;
  saveChanges: () => void;
  isSaving: boolean;
  saveFailed: boolean;
  addPage: () => void;
  setContent: (pageId: string, content: string) => void;
  removePage: (pageId: string) => void;
  movePageUp: (pageId: string) => void;
  movePageDown: (pageId: string) => void;
  renamePage: (pageId: string, title: string) => void;
  isDirty: boolean;
}>({
  localData: null,
  saveChanges: () => {},
  isSaving: false,
  saveFailed: false,
  addPage: () => {},
  setContent: () => {},
  removePage: () => {},
  movePageUp: () => {},
  movePageDown: () => {},
  renamePage: () => {},
  isDirty: false,
});

enum ActionType {
  LoadData = "SET_REMOTE_DATA",
  AddPage = "ADD_PAGE",
  SetContent = "SET_CONTENT",
  RemovePage = "REMOVE_PAGE",
  MovePageUp = "MOVE_PAGE_UP",
  MovePageDown = "MOVE_PAGE_DOWN",
  RenamePage = "RENAME_PAGE",
}

const reducer = (state: State, action) => {
  switch (action.type) {
    case ActionType.LoadData: {
      return {
        ...action.payload,
        pages: action.payload.pages.map((page) => ({
          ...page,
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
    case ActionType.RenamePage: {
      const { pageId, title } = action.payload;
      return {
        ...state,
        pages: state.pages.map((page) =>
          page.id === pageId ? { ...page, title } : page,
        ),
      };
    }
  }
  return state;
};

export const useLocalData = () => {
  return useContext(LocalStateContext);
};

const removeTypenames = (obj) => {
  if (Array.isArray(obj)) {
    return obj.map(removeTypenames);
  }

  if (obj !== null && typeof obj === "object") {
    const newObj = {};
    for (const key in obj) {
      if (key !== "__typename") {
        newObj[key] = removeTypenames(obj[key]);
      }
    }

    return newObj;
  }

  return obj;
};

const useLoadRemoteData = (dispatch) => {
  const { documentId } = useArgs();

  const { data } = useInvitationLetterDocumentSuspenseQuery({
    variables: {
      id: documentId,
    },
  });

  useEffect(() => {
    const dynamicDocument = data?.invitationLetterDocument.dynamicDocument;
    dispatch({
      type: ActionType.LoadData,
      payload: removeTypenames(dynamicDocument),
    });
  }, [data]);

  const remoteData = useMemo(() => {
    return removeTypenames(data?.invitationLetterDocument.dynamicDocument);
  }, [data]);

  return remoteData;
};

const useSaveRemoteData = (): [(newData) => void, boolean, boolean] => {
  const [updateInvitationLetter, { loading: savingChanges, error }] =
    useUpdateInvitationLetterDocumentMutation();
  const { documentId } = useArgs();

  return [
    (newData) => {
      updateInvitationLetter({
        variables: {
          input: {
            id: documentId,
            dynamicDocument: newData,
          },
        },
      });
    },
    savingChanges,
    !!error,
  ];
};

export const LocalStateProvider = ({ children }) => {
  const [localData, dispatch] = useReducer<State, any>(reducer, null);
  const remoteData = useLoadRemoteData(dispatch);
  const [saveChanges, isSaving, saveFailed] = useSaveRemoteData();

  const isDirty = !equal(remoteData, localData);

  return (
    <LocalStateContext.Provider
      value={{
        localData: localData || remoteData,
        isDirty,
        saveChanges: () => saveChanges(localData),
        isSaving,
        saveFailed,
        addPage: () => dispatch({ type: ActionType.AddPage }),
        renamePage: (pageId, title) => {
          dispatch({
            type: ActionType.RenamePage,
            payload: { pageId, title },
          });
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
