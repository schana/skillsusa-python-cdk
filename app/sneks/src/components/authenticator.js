import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";

import { Authenticator, useAuthenticator } from "@aws-amplify/ui-react";

export default function AuthGuard(props) {
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);
  return authStatus !== "authenticated" ? (
    <ContentLayout
      header={
        <Header
          variant="h1"
          description="Contact your contest coordinator with issues"
        >
          Sign in to access contestant tools
        </Header>
      }
    >
      <Authenticator hideSignUp={true} loginMechanisms={["email"]} />
    </ContentLayout>
  ) : (
    props.children
  );
}
