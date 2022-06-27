import * as cheerio from "cheerio";
import * as fs from "node:fs/promises";
import * as pathModule from "node:path";
import * as S3 from "aws-sdk/clients/s3";

const BASE_OUTPUT_PATH = "output";

const PAGES_TO_IGNORE = [
  "/en/login",
  "/it/login",
  "/en/tickets",
  "/it/tickets",
  "/it/",
  "/en/",
  "/en/_error",
  "/it/_error",
];

const VISITED_URLS = new Set();
const S3_CLIENT = new S3();

const scape = async (url: string, host: string) => {
  console.log(`Scraping: ${url}`);
  try {
    const response = await fetch(url);

    const path = url.replace(host, "");
    const body = await response.text();

    const parsableBody = cheerio.load(body);

    const newUrls = await findUrls(parsableBody);

    await storeImages(parsableBody);
    await storeContent(path, parsableBody.html());

    // const promises = [];

    for (const newUrl of newUrls) {
      // promises.push(scape(`${host}${newUrl}`, host));
      await scape(`${host}${newUrl}`, host);
    }

    // await Promise.all(promises);
  } catch (e) {
    console.log("Error while scraping", e);
  }
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

const storeContent = async (path: string, body: string) => {
  let finalPath;
  let contentType;

  // if (path.endsWith(".js")) {
  //   finalPath = `${BASE_OUTPUT_PATH}/${path}`;
  // } else {
  //   finalPath = `${BASE_OUTPUT_PATH}/${path}/index.html`;
  // }
  if (path.endsWith(".js")) {
    finalPath = path;
    contentType = "application/javascript";
  } else {
    finalPath = `${path.slice(1)}/index.html`;
    contentType = "text/html";
  }

  // await fs.mkdir(pathModule.dirname(finalPath), { recursive: true });
  // await fs.writeFile(finalPath, body);

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
  const links = body("a, script");
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
