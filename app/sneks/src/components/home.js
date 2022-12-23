// https://youtu.be/L73WY-IT2sE

import * as React from "react";

import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";

export default function Home() {
  const videos = [
    "game_bd1fc2d1-cf38-4f4a-bdbc-d2f0afb5302d.mp4",
    "game_2ad4911c-b98b-4bc6-9397-c9d6ec8ee3cd.mp4",
    "game_180a10bf-8c99-4d80-b730-b16b0ac6a130.mp4",
    "game_75b00efc-c7b9-4cfe-bd57-05d278f4e635.mp4",
    "game_9618bfa5-a587-4503-a78f-5e4de6aaed5d.mp4",
    "game_c5a547a4-aa96-4d09-b014-e2e04b84c654.mp4",
    "game_db138f75-fab2-4273-bb70-5055971ae260.mp4",
    "game_fada956c-e684-4b57-a1ff-42080c0abf1b.mp4",
  ];
  const [src, setSrc] = React.useState(0);
  const videoRef = React.useRef(null);

  const onEnded = () => {
    setSrc((src + 1) % videos.length);
    videoRef.current.load();
  };

  return (
    <ContentLayout
      header={
        <Header variant="h1" description="Latest submission runs">
          Sneks
        </Header>
      }
    >
      <video
        ref={videoRef}
        onEnded={onEnded}
        width="100%"
        height="auto"
        autoPlay
        muted
      >
        <source
          src={`https://www.sneks.dev/games/${videos[src]}`}
          type="video/mp4"
        />
      </video>
    </ContentLayout>
  );
}
