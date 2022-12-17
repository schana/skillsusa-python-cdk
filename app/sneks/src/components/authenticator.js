import * as React from "react";
import Container from "@cloudscape-design/components/container";
import Header from "@cloudscape-design/components/header";

import { Authenticator, useAuthenticator } from "@aws-amplify/ui-react";

export default function AuthGuard(props) {
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);
  return authStatus !== "authenticated" ? (
    <Container
      header={<Header variant="h2">Sign in to access contestant tools</Header>}
    >
      <Authenticator hideSignUp={true} loginMechanisms={["email"]} />
    </Container>
  ) : (
    props.children
  );
}
