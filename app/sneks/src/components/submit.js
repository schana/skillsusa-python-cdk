import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";
import { FileUploader } from "@aws-amplify/ui-react";
import { Storage } from "aws-amplify";
import { Auth } from "aws-amplify";

import AuthGuard from "./authenticator";

export default function Submit() {
  const onSuccess = ({ key }) => {
    Auth.currentAuthenticatedUser()
      .then((attributes) => {
        Storage.put(
          "user_info.py",
          `
# ${attributes.attributes.email}
# ${attributes.attributes.sub}
          `,
          {
            level: "private",
          }
        );
      })
      .catch((err) => console.log(err));
  };

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
          maxSize={20000}
          useAccelerateEndpoint={true}
          onSuccess={onSuccess}
        />
      </ContentLayout>
    </AuthGuard>
  );
}
