import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";

import AuthGuard from "./authenticator";

export default function Scores() {
  return (
    <AuthGuard>
      <ContentLayout
        header={
          <Header variant="h1" description="header description">
            Scores
          </Header>
        }
      >
        <Container
          header={
            <Header variant="h2" description="container description">
              container header
            </Header>
          }
        >
          scores
        </Container>
      </ContentLayout>
    </AuthGuard>
  );
}
