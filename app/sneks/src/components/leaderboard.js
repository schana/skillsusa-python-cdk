import * as React from "react";
import Table from "@cloudscape-design/components/table";
import Box from "@cloudscape-design/components/box";
import { useCollection } from "@cloudscape-design/collection-hooks";
import { Auth } from "aws-amplify";
import { useAuthenticator } from "@aws-amplify/ui-react";

export default function Leaderboard({ scores, colors, timestamp }) {
  const [identityId, setIdentityId] = React.useState("not loaded");
  const { authStatus } = useAuthenticator((context) => [context.authStatus]);

  React.useEffect(() => {
    if (authStatus === "authenticated") {
      Auth.currentUserCredentials()
        .then((result) => {
          setIdentityId(result.identityId);
        })
        .catch((err) => console.log(err));
    }
  }, [authStatus]);

  const { items, collectionProps } = useCollection(scores, {
    sorting: {},
  });

  const definitions = [
    {
      id: "color",
      header: "Color",
      cell: (e) => (
        <div
          style={{
            background: `linear-gradient(to right, rgb(${
              colors[e.name].body
            }) 75%, rgb(${colors[e.name].head}) 25%)`,
          }}
        >
          &nbsp;
        </div>
      ),
    },
  ];

  if (authStatus === "authenticated") {
    definitions.push({
      id: "name",
      header: "Name",
      cell: (e) =>
        e.name.startsWith(identityId) ? Auth.user.attributes.email : "",
    });
  }
  definitions.push(
    {
      id: "age",
      header: "Age",
      cell: (e) => e.age.toLocaleString(),
      sortingField: "age",
    },
    {
      id: "length",
      header: "Length",
      cell: (e) => e.length.toLocaleString(),
      sortingField: "length",
    },
    {
      id: "ended",
      header: "Ended",
      cell: (e) => e.ended.toLocaleString(),
      sortingField: "ended",
    },
    {
      id: "age1",
      header: "Age'",
      cell: (e) => e.age1.toLocaleString(),
      sortingField: "age1",
    },
    {
      id: "length1",
      header: "Length'",
      cell: (e) => e.length1.toLocaleString(),
      sortingField: "length1",
    },
    {
      id: "ended1",
      header: "Ended'",
      cell: (e) => e.ended1.toLocaleString(),
      sortingField: "ended1",
    },
    {
      id: "score",
      header: "Score",
      cell: (e) => (e.age1 + e.length1 + e.ended1).toLocaleString(),
      sortingField: "score",
    }
  );

  return (
    <Table
      items={items}
      {...collectionProps}
      columnDefinitions={definitions}
      variant="embedded"
      trackBy="name"
      empty={
        <Box textAlign="center" color="inherit">
          <b>No submissions</b>
          <Box padding={{ bottom: "s" }} variant="p" color="inherit">
            Nothing has been uploaded yet
          </Box>
        </Box>
      }
      footer={<Box>Last updated: {timestamp}</Box>}
    />
  );
}
