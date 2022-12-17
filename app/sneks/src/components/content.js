import * as React from "react";
import { useRoutes, Navigate } from "react-router-dom";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import { FileUploader } from "@aws-amplify/ui-react";

import AuthGuard from "./authenticator";

export default function Content() {
  const element = useRoutes([
    {
      path: "/",
      element: (
        <ContentLayout
          header={
            <Header variant="h1" description="header description">
              Home
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
            home
          </Container>
        </ContentLayout>
      ),
    },
    {
      path: "signin",
      element: (
        <AuthGuard>
          <Navigate to="/" replace={true} />
        </AuthGuard>
      ),
    },
    {
      path: "scores",
      element: (
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
      ),
    },
    {
      path: "submit",
      element: (
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
              acceptedFileTypes={[".py", ".txt"]}
              variation="drop"
            />
          </ContentLayout>
        </AuthGuard>
      ),
    },
  ]);

  return <ContentLayout>{element}</ContentLayout>;
}
