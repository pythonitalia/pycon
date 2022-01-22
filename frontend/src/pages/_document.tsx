import React from "react";
import { InitializeColorMode } from "theme-ui";

import Document, { Head, Html, Main, NextScript } from "next/document";
import Script from "next/script";

export default class MyDocument extends Document<{
  ids: string[];
  css: string;
  url: string;
}> {
  render() {
    return (
      <Html>
        <Head>
          <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
          <link rel="shortcut icon" href="/favicon.png" />

          <script
            async={true}
            defer={true}
            data-domain="pycon.it"
            src="https://plausible.io/js/plausible.js"
          />
        </Head>
        <body>
          <InitializeColorMode />
          <Main />
          <NextScript />
          <Script
            strategy="afterInteractive"
            dangerouslySetInnerHTML={{
              __html: `
;(function(o,l,a,r,k,y){if(o.olark)return;
r="script";y=l.createElement(r);r=l.getElementsByTagName(r)[0];
y.async=1;y.src="//"+a;r.parentNode.insertBefore(y,r);
y=o.olark=function(){k.s.push(arguments);k.t.push(+new Date)};
y.extend=function(i,j){y("extend",i,j)};
y.identify=function(i){y("identify",k.i=i)};
y.configure=function(i,j){y("configure",i,j);k.c[i]=j};
k=y._={s:[],t:[+new Date],c:{},l:a};
})(window,document,"static.olark.com/jsclient/loader.js");
/* Add configuration calls below this comment */
olark.identify('1751-12112149-10-1389');`,
            }}
          />
        </body>
      </Html>
    );
  }
}
