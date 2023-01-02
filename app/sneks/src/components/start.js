import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";
import Link from "@cloudscape-design/components/link";
import ExpandableSection from "@cloudscape-design/components/expandable-section";

import AuthGuard from "./authenticator";

export default function Start() {
  return (
    <AuthGuard>
      <ContentLayout
        header={
          <Header
            variant="h1"
            description="Documentation and resources to begin your Snek's journey"
          >
            Getting started
          </Header>
        }
      >
        <Container>
          <h2>Where to begin</h2>
          <p>
            Follow the{" "}
            <Link href="/docs/index.html">getting started guide</Link> to start
            making your Snek. When your Snek is ready,{" "}
            <Link href="/submit">upload</Link> your <code>submission.py</code>{" "}
            to have it evaluated.
          </p>
          <h2>FAQ</h2>
          <ExpandableSection headerText="What if my question isn't here?">
            Reach out to your contest coordinator or{" "}
            <Link external href="mailto:admin@sneks.dev">
              email the admin
            </Link>
            .
          </ExpandableSection>
        </Container>
      </ContentLayout>
    </AuthGuard>
  );
}
