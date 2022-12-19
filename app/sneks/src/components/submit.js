import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";
import { FileUploader } from "@aws-amplify/ui-react";

import AuthGuard from "./authenticator";

export default function Submit() {
  return (
    <AuthGuard>
      <ContentLayout
        header={
          <Header
            variant="h1"
            description="You can upload as many times as you want during the competition"
          >
            Upload your submission
          </Header>
        }
      >
        <FileUploader
          accessLevel="private"
          variation="drop"
          acceptedFileTypes={[".py"]}
          maxFiles={20}
          maxSize={10000}
        />
      </ContentLayout>
    </AuthGuard>
  );
}
