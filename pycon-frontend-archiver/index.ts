import * as cheerio from "cheerio";
import * as fs from "node:fs/promises";
import * as pathModule from "node:path";
import * as S3 from "aws-sdk/clients/s3";

const BASE_OUTPUT_PATH = "output";

const SITE_URL = "https://pycon.it";
const CDN_URL = "https://cdn.pycon.it/";

type Type = "document" | "style" | "script";

const PAGES_TO_IGNORE = [
  "/en/profile/edit",
  "/it/profile/edit",
  "/en/profile",
  "/it/profile",
  "/en/signup",
  "/it/signup",
  "/en/login",
  "/it/login",
  "/en/tickets",
  "/it/tickets",
  "/en/",
  "/en/_error",
  "/it/_error",
];

const VISITED_URLS = new Set();
const S3_CLIENT = new S3();

const scape = async (url: string, host: string) => {
  try {
    if (VISITED_URLS.has(url)) {
      console.log(`Ignoring: ${url}`);
      return;
    }

    console.log(`Scraping: ${url}`);

    const response = await fetch(url);

    const path = url.replace(host, "");
    let type: Type;
    if (path.endsWith(".js")) {
      type = "script";
    } else if (path.endsWith(".css")) {
      type = "style";
    } else {
      type = "document";
    }
    const body = await response.text();

    const parsableBody = cheerio.load(body);

    const newUrls = await findUrls(parsableBody);

    await storeImages(parsableBody);
    await storeContent(
      path,
      type !== "document" ? body : parsableBody.html(),
      type,
    );

    await discoverHiddenLinks(parsableBody, newUrls);

    for (const newUrl of newUrls) {
      await scape(`${host}${newUrl}`, host);
    }
  } catch (e) {
    console.log("Error while scraping", e);
  }
};

const discoverHiddenLinks = async (
  body: cheerio.CheerioAPI,
  urls: Set<string>,
) => {
  const nextDataPayload = body('script[id="__NEXT_DATA__"]');

  if (nextDataPayload.length > 0) {
    try {
      const parsedPayload = JSON.parse(nextDataPayload.first().text());
      const apolloState = parsedPayload.props.pageProps.__APOLLO_STATE__;
      for (const [key, item] of Object.entries<any>(apolloState)) {
        if (!key.startsWith("Conference")) {
          continue;
        }

        const conferenceNavMenu = item['menu({"identifier":"conference-nav"})'];
        await extractMenuLinks(conferenceNavMenu, urls);

        const programNavMenu = item['menu({"identifier":"program-nav"})'];
        await extractMenuLinks(programNavMenu, urls);
      }
    } catch (e) {
      console.log("Unable to parse next payload: ", e);
    }
  }
};

const extractMenuLinks = async (menu: any, urls: Set<string>) => {
  const links = menu.links;
  for (const link of links) {
    const href = link['href({"language":"en"})'];

    const enHref = `/en${href}`;
    const itHref = `/it${href}`;

    if (!VISITED_URLS.has(itHref)) {
      urls.add(itHref);
      VISITED_URLS.add(itHref);
      continue;
    }

    if (!VISITED_URLS.has(enHref)) {
      urls.add(enHref);
      VISITED_URLS.add(enHref);
      continue;
    }
  }
};

const downloadImage = async (src: string): Promise<string> => {
  const filename = src.replace(CDN_URL, "");
  const response = await fetch(src);
  const path = `images/${filename}`;

  await S3_CLIENT.putObject(
    {
      Key: path,
      Bucket: "pycon-archive-test-website",
      Body: Buffer.from(await response.arrayBuffer()),
      ContentType: `image/${pathModule.extname(path).slice(1)}`,
      ACL: "public-read",
    },
    undefined,
  ).promise();
  return `/images/${filename}`;
};

const storeContent = async (path: string, body: string, type: Type) => {
  let finalPath;
  let contentType;

  path = decodeURI(path.slice(1));
  if (type === "script") {
    finalPath = path;
    contentType = "application/javascript";
  } else if (type === "style") {
    finalPath = path;
    contentType = "text/css";
  } else {
    finalPath = `${path}/index.html`;
    contentType = "text/html";
  }

  await S3_CLIENT.putObject(
    {
      Key: finalPath,
      Bucket: "2022.pycon.it",
      Body: body,
      ContentType: contentType,
      ACL: "public-read",
    },
    undefined,
  ).promise();
};

const findUrls = async (body: cheerio.CheerioAPI) => {
  const links = body('a, script, link[rel="stylesheet"]');
  const urlsFound: Set<string> = new Set();

  for (const linkElement of links) {
    const attrLink = linkElement.attribs.href ?? linkElement.attribs.src;

    if (!attrLink) {
      continue;
    }

    const link = attrLink.split("?")[0];

    if (link.startsWith("http") || link.startsWith("mailto")) {
      continue;
    }

    if (PAGES_TO_IGNORE.includes(link)) {
      continue;
    }

    if (VISITED_URLS.has(link)) {
      continue;
    }

    VISITED_URLS.add(link);
    urlsFound.add(link);
  }

  return urlsFound;
};

(async () => {
  try {
    await fs.rm(BASE_OUTPUT_PATH, { recursive: true });
  } catch (e) {}

  await fs.mkdir(BASE_OUTPUT_PATH);

  await scape("https://pycon.it/en", SITE_URL);
})();
