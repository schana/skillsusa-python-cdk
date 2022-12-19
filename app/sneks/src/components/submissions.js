import * as React from "react";
import ContentLayout from "@cloudscape-design/components/content-layout";
import Header from "@cloudscape-design/components/header";
import Table from "@cloudscape-design/components/table";
import Box from "@cloudscape-design/components/box";
import Button from "@cloudscape-design/components/button";
import SpaceBetween from "@cloudscape-design/components/space-between";
import { Storage } from "aws-amplify";
import { useCollection } from "@cloudscape-design/collection-hooks";

import AuthGuard from "./authenticator";
import Preview from "./preview";

export default function Submissions({ colorMode }) {
  const [loading, setLoading] = React.useState(true);
  const [files, setFiles] = React.useState([]);
  const [previewKey, setPreviewKey] = React.useState("");

  React.useEffect(() => {
    Storage.vault
      .list("", { pageSize: "ALL" })
      .then((result) => {
        setFiles(result.results.filter((file) => file.size > 0));
        setLoading(false);
      })
      .catch((err) => console.log(err));
  }, []);

  const { items, collectionProps } = useCollection(files, {
    sorting: {},
  });

  const downloadFile = (key) => {
    Storage.vault
      .get(key)
      .then((result) => {
        window.open(result, "_blank");
      })
      .catch((err) => console.log(err));
  };

  return (
    <AuthGuard>
      <ContentLayout
        header={
          <Header variant="h1" description="View and download your submissions">
            Your submissions
          </Header>
        }
      >
        <Preview
          objectKey={previewKey}
          setObjectKey={setPreviewKey}
          colorMode={colorMode}
        />
        <Table
          items={items}
          {...collectionProps}
          columnDefinitions={[
            {
              id: "key",
              header: "Name",
              cell: (e) => e.key,
              sortingField: "key",
            },
            {
              id: "lastModified",
              header: "Last Modified",
              cell: (e) => e.lastModified.toLocaleString(),
              sortingField: "lastModified",
            },
            {
              id: "size",
              header: "Size",
              cell: (e) => e.size,
              sortingField: "size",
            },
            {
              id: "download",
              header: (
                <Box float="right" variant="awsui-key-label">
                  Access
                </Box>
              ),
              cell: (item) => (
                <Box float="right">
                  <SpaceBetween direction="horizontal" size="xs">
                    <Button
                      variant="normal"
                      iconName="script"
                      onClick={() => setPreviewKey(item.key)}
                    />
                    <Button
                      variant="primary"
                      iconName="download"
                      onClick={() => downloadFile(item.key)}
                    />
                  </SpaceBetween>
                </Box>
              ),
            },
          ]}
          loading={loading}
          loadingText="Loading"
          variant="container"
          trackBy="key"
          empty={
            <Box textAlign="center" color="inherit">
              <b>No submissions</b>
              <Box padding={{ bottom: "s" }} variant="p" color="inherit">
                Nothing has been uploaded yet
              </Box>
              <Button>Upload submission</Button>
            </Box>
          }
        />
      </ContentLayout>
    </AuthGuard>
  );
}
