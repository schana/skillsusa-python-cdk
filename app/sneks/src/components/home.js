// https://youtu.be/L73WY-IT2sE

import * as React from "react";

import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";

export default function Home() {
  return (
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
  );
}
