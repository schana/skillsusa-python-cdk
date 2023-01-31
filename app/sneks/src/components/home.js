import * as React from "react";

import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";

import Leaderboard from "./leaderboard";

export default function Home() {
  const [videos, setVideos] = React.useState([]);
  const [scores, setScores] = React.useState([]);
  const [colors, setColors] = React.useState([]);
  const [timestamp, setTimestamp] = React.useState([]);
  const [src, setSrc] = React.useState(0);
  const videoRef = React.useRef(null);

  React.useEffect(() => {
    fetch("games/manifest.json")
      .then((response) => response.json())
      .then((responseJson) => {
        setVideos(responseJson.videos);
        setScores(responseJson.scores);
        setColors(responseJson.colors);
        setTimestamp(
          new Date(`${responseJson.timestamp}+0000`).toLocaleString()
        );
        setSrc(Math.floor(Math.random() * responseJson.videos.length));
        videoRef.current.load();
      })
      .catch((err) => console.log(err));
  }, []);

  const onEnded = () => {
    setSrc((src + 1) % videos.length);
    videoRef.current.load();
  };

  return (
    <ContentLayout header={<Header />}>
      <video
        ref={videoRef}
        onEnded={onEnded}
        width="100%"
        height="auto"
        autoPlay
        muted
        playsInline
        poster="poster.png"
        src={
          videos.length > 0
            ? videos[src]
            : `https://www.sneks.dev/games/game_29d61406-c7a4-41a0-884c-d6a165ac3353.mp4`
        }
        type="video/mp4"
      />
      <Leaderboard scores={scores} colors={colors} timestamp={timestamp} />
    </ContentLayout>
  );
}
