import { useApolloClient } from "@apollo/client";
import React from "react";
import { CSSProperties } from "react";

import { ScheduleItemFragment } from "./schedule-item.generated";

type Props = {
  style?: CSSProperties;
  item: ScheduleItemFragment;
};

export const ItemCard = React.forwardRef(({ style, item }: Props, ref: any) => {
  const apolloClient = useApolloClient();
  const audienceLevel =
    item.audienceLevel?.name ?? item.submission?.audienceLevel?.name;
  const header = [audienceLevel, item.type].filter((v) => !!v).join(" ");

  const openEditLink = (e) => {
    e.preventDefault();

    const baseUrl =
      document.location.ancestorOrigins?.[0] || document.location.origin;

    const editorWindow = window.open(
      `${baseUrl}/admin/schedule/scheduleitem/${item.id}`,
      "Editor",
      "width=800,height=600",
    );
    console.log("editorWindow", editorWindow);
    if (editorWindow) {
      editorWindow.addEventListener("beforeunload", () => {
        console.log("unload");
        apolloClient.refetchQueries({
          include: ["ScheduleQuery"],
        });
      });
    }
  };

  return (
    <div ref={ref} className="bg-slate-200 p-3 z-50" style={style}>
      <span className="block">[{header}]</span>
      <span className="block my-4">{item.title}</span>
      <span className="block font-bold">
        {item.speakers.map((speaker) => speaker.fullName).join(", ")}
      </span>
      <a className="underline" href="#" onClick={openEditLink}>
        Edit schedule item
      </a>
    </div>
  );
});
