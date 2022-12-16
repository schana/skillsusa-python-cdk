import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import Button from "@cloudscape-design/components/button";
import { Authenticator, FileUploader } from '@aws-amplify/ui-react';

import SneksHeader from "./header";

export default () => {
  return (
    <ContentLayout
      header={<SneksHeader />}
    >
      <Container
        header={
          <Header
            variant="h2"
            description="Container description"
          >
            Container header
          </Header>
        }
      >
        <Authenticator hideSignUp={true}>
         {({ signOut, user }) => (
            <div>
              <FileUploader
                accessLevel="private"
                acceptedFileTypes={['.py', '.txt']}
                variation="drop"
              />
              <p>
                Welcome, {user.username}.
              </p>
              <Button onClick={signOut}>Sign out</Button>
            </div>
        )}
        </Authenticator>
      </Container>
    </ContentLayout>
  );
}