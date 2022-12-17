//import { useState } from "react";

import AppLayout from "@cloudscape-design/components/app-layout";

import Navigation from "./components/navigation";
import Notifications from "./components/notifications";
import Content from "./components/content";
import Tools from "./components/tools";

import SneksHeader from "./components/header";

import "./App.css";

export default function App() {
  //  const [toolsOpen, setToolsOpen] = useState(true);
  return (
    <>
      <div id="h" style={{ position: "sticky", top: 0, zIndex: 1002 }}>
        <SneksHeader />
      </div>
      <AppLayout
        headerSelector="#h"
        //        toolsOpen={toolsOpen}
        //        onToolsChange={(evt) => setToolsOpen(evt.detail.open)}
        navigation={<Navigation />}
        notifications={<Notifications />}
        tools={<Tools />}
        content={<Content />}
      />
    </>
  );
}
