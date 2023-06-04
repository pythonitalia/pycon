import { ParsedUrlQuery } from "querystring";

export const createHref = ({
  path,
  params,
  locale,
  external,
}: {
  path: string;
  params?: ParsedUrlQuery;
  locale: string;
  external?: boolean;
}) => {
  if (external) {
    return path;
  }

  const { resolvedPath, unusedParams } = Object.entries(params || {}).reduce(
    (state, [key, value]) => {
      const newPath = state.resolvedPath.replace(`[${key}]`, value as string);

      if (newPath === state.resolvedPath) {
        state.unusedParams[key] = value;
        return state;
      }

      state.resolvedPath = newPath;
      return state;
    },
    {
      resolvedPath: path,
      unusedParams: {},
    },
  );

  const queryParams = Object.entries(unusedParams)
    .map(([key, value]) => `${key}=${value}`)
    .join("&");

  return `/${locale}${resolvedPath}${
    queryParams.length > 0 ? `?${queryParams}` : ""
  }`;
};
