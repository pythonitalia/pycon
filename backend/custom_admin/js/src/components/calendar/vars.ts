export const getVars = () => {
  const params = new URLSearchParams(window.location.search);
  return {
    apolloGraphQLUrl: fixParamAndFallback(
      (window as any).apolloGraphQLUrl,
      "{{ GATEWAY_GRAPHQL_URL }}",
      params.get("GATEWAY_GRAPHQL_URL"),
    ),
    conferenceCode: fixParamAndFallback(
      (window as any).conferenceCode,
      "{{ CONFERENCE_CODE }}",
      params.get("CONFERENCE_CODE"),
    ),
  };
};

const fixParamAndFallback = (
  param: string,
  placeholder: string,
  fallback: string,
): string => {
  return param.replace(placeholder, "") || fallback;
};
