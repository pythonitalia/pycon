import { getApolloClient } from "~/apollo/client";
import { queryPagePreview } from "~/types";

export default async (req, res) => {
  const contentType = req.query.content_type;
  const token = req.query.token;

  const apolloClient = getApolloClient();
  const response = await queryPagePreview(apolloClient, {
    contentType: contentType,
    token: token,
  });

  if (response.error || !response.data || response.data.pagePreview === null) {
    return res.status(401).json({ message: "Invalid token" });
  }

  res.setPreviewData(
    {
      contentType: contentType,
      token: token,
    },
    {
      // very short age because we don't need to left it alive for long
      // as wagtail will generate new token on each preview request
      maxAge: 3,
    },
  );
  res.redirect("/");
};
