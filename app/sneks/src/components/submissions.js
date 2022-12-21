import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";
import Tabs from "@cloudscape-design/components/tabs";

import AuthGuard from "./authenticator";
import Files from "./files";
import { useLocalStorage } from "../hooks";

export default function Submissions({ colorMode }) {
  const [activeTabId, setActiveTabId] = useLocalStorage("submitted");

  return (
    <AuthGuard>
      <ContentLayout
        header={
          <Header variant="h1" description="View and download your submissions">
            Your submissions
          </Header>
        }
      >
        <Tabs
          onChange={({ detail }) => setActiveTabId(detail.activeTabId)}
          activeTabId={activeTabId}
          tabs={[
            {
              label: "Uploaded",
              id: "uploaded",
              content: <Files colorMode={colorMode} prefix={"private/"} />,
            },
            {
              label: "Processing",
              id: "processing",
              content: <Files colorMode={colorMode} prefix={"processing/"} />,
            },
            {
              label: "Submitted",
              id: "submitted",
              content: <Files colorMode={colorMode} prefix={"submitted/"} />,
            },
            {
              label: "Invalid",
              id: "invalid",
              content: <Files colorMode={colorMode} prefix={"invalid/"} />,
            },
          ]}
          variant="container"
        />
      </ContentLayout>
    </AuthGuard>
  );
}
