import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import Button from "@cloudscape-design/components/button";
import {
  Authenticator,
  FileUploader,
  useAuthenticator,
} from "@aws-amplify/ui-react";

export default () => {
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);
  return (
    <ContentLayout>
      {authStatus === "configuring" && "Loading..."}
      {authStatus !== "authenticated" ? (
        <Container
          header={
            <Header variant="h2">
              Sign in to access the submission uploader
            </Header>
          }
        >
          <Authenticator hideSignUp={true} />
        </Container>
      ) : (
        <Container
          header={
            <Header
              variant="h2"
              description="You can upload as many times as you want during the competition"
            >
              Upload your submission
            </Header>
          }
        >
          <FileUploader
            accessLevel="private"
            acceptedFileTypes={[".py", ".txt"]}
            variation="drop"
          />
        </Container>
      )}
    </ContentLayout>
  );
};
