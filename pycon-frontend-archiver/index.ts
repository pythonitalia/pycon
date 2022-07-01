import * as cheerio from "cheerio";
import * as fs from "node:fs/promises";
import * as pathModule from "node:path";
import * as S3 from "aws-sdk/clients/s3";

const BASE_OUTPUT_PATH = "output";

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
  console.log(`Scraping: ${url}`);
  try {
    const response = await fetch(`${url}?archive=1`);

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

    await removeUnavailableContent(parsableBody);
    await storeImages(parsableBody);
    await storeContent(
      path,
      type !== "document" ? body : parsableBody.html(),
      type,
    );

    for (const newUrl of newUrls) {
      await scape(`${host}${newUrl}`, host);
    }
  } catch (e) {
    console.log("Error while scraping", e);
  }
};

const removeUnavailableContent = async (body: cheerio.CheerioAPI) => {
  const ticketsLink = body('a[href="/en/tickets"],a[href="/it/tickets"]');
  ticketsLink.remove();

  const loginButton = body('a[href="/en/login"],a[href="/it/login"]');
  loginButton.remove();
};

const storeImages = async (body: cheerio.CheerioAPI) => {
  const images = body("img");
  for (const image of images) {
    const src = image.attribs.src;

    if (!src.startsWith("https://cdn.pycon.it/")) {
      continue;
    }

    const newSrc = await downloadImage(src);
    image.attribs.src = newSrc;
  }
};

const downloadImage = async (src: string): Promise<string> => {
  const filename = src.replace("https://cdn.pycon.it/", "");
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

  path = path.slice(1);
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
      Bucket: "pycon-archive-test-website",
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

  await scape("https://pycon.it/en", "https://pycon.it");
})();
