// https://youtu.be/L73WY-IT2sE

import * as React from "react";

import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";

export default function Home() {
  const [videos, setVideos] = React.useState([]);
  const [src, setSrc] = React.useState(0);
  const videoRef = React.useRef(null);

  React.useEffect(() => {
    fetch("games/manifest.json")
      .then((response) => response.json())
      .then((responseJson) => {
        setVideos(responseJson.videos);
        videoRef.current.load();
      });
  }, []);

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
        poster="poster.png"
      >
        <source src={videos[src]} type="video/mp4" />
      </video>
    </ContentLayout>
  );
}
