import * as React from "react";

import { useLocalStorage } from "./hooks";

import { ThemeProvider, defaultDarkModeOverride } from "@aws-amplify/ui-react";

import { applyMode, Mode } from "@cloudscape-design/global-styles";
import AppLayout from "@cloudscape-design/components/app-layout";

import "@cloudscape-design/global-styles/index.css";
import "@cloudscape-design/global-styles/dark-mode-utils.css";
import "@aws-amplify/ui-react/styles.css";

import Navigation from "./components/navigation";
import Notifications from "./components/notifications";
import Content from "./components/content";
import Tools from "./components/tools";

import SneksHeader from "./components/header";

export default function App() {
  const theme = {
    name: "my-theme",
    overrides: [defaultDarkModeOverride],
  };
  const [amplifyColorMode, setAmplifyColorMode] = useLocalStorage(
    "mode",
    "light"
  );
  if (amplifyColorMode === "dark") {
    applyMode(Mode.Dark);
  } else {
    applyMode(Mode.Light);
  }

  function setMode(mode) {
    if (mode === "dark") {
      setAmplifyColorMode(mode);
      applyMode(Mode.Dark);
    } else {
      setAmplifyColorMode(mode);
      applyMode(Mode.Light);
    }
  }

  const [toolsOpen, setToolsOpen] = useLocalStorage("toolsOpen", false);
  const [navOpen, setNavOpen] = useLocalStorage("navOpen", false);
  return (
    <ThemeProvider theme={theme} colorMode={amplifyColorMode}>
      <div id="h" style={{ position: "sticky", top: 0, zIndex: 1002 }}>
        <SneksHeader setMode={setMode} mode={amplifyColorMode} />
      </div>
      <AppLayout
        headerSelector="#h"
        toolsOpen={toolsOpen}
        onToolsChange={(evt) => setToolsOpen(evt.detail.open)}
        navigationOpen={navOpen}
        onNavigationChange={(evt) => setNavOpen(evt.detail.open)}
        navigation={<Navigation />}
        notifications={<Notifications />}
        tools={<Tools />}
        content={<Content colorMode={amplifyColorMode} />}
      />
    </ThemeProvider>
  );
}
