import { useState } from "react";

import { Amplify } from "aws-amplify";
import { Authenticator } from "@aws-amplify/ui-react";

import AppLayout from "@cloudscape-design/components/app-layout";

import Content from "./components/content";
import Navigation from "./components/navigation";
import Tools from "./components/tools";
import Notifications from "./components/notifications";

import "@cloudscape-design/global-styles/index.css";
import "@aws-amplify/ui-react/styles.css";
import "./App.css";

import SneksHeader from "./components/header";

Amplify.configure({
  Auth: {
    region: "us-east-1", // REQUIRED - Amazon Cognito Region
    userPoolId: "us-east-1_5qPGQ7PVq", //OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: "5ffs1d5kpodcljl7in0jj771fm",
  },
  Storage: {
    AWSS3: {
      bucket: "",
      region: "us-east-1",
    },
  },
});

export default function App() {
  const [toolsOpen, setToolsOpen] = useState(true);
  return (
    <Authenticator.Provider>
      <div id="h" style={{ position: "sticky", top: 0, zIndex: 1002 }}>
        <SneksHeader />
      </div>
      <AppLayout
        headerSelector="#h"
        toolsOpen={toolsOpen}
        onToolsChange={(evt) => setToolsOpen(evt.detail.open)}
        navigation={<Navigation />}
        notifications={<Notifications />}
        tools={<Tools />}
        content={<Content />}
      />
    </Authenticator.Provider>
  );
}
