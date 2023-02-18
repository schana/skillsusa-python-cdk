import * as React from "react";
import Table from "@cloudscape-design/components/table";
import Box from "@cloudscape-design/components/box";
import Button from "@cloudscape-design/components/button";
import SpaceBetween from "@cloudscape-design/components/space-between";
import { Storage } from "aws-amplify";
import { useCollection } from "@cloudscape-design/collection-hooks";
import { useNavigate } from "react-router-dom";

import Preview from "./preview";

function formatBytes(bytes) {
  let descriptor = "bytes";
  if (bytes > 1024) {
    bytes = bytes / 1024;
    descriptor = "KiB";
  }
  if (bytes > 1024) {
    bytes = bytes / 1024;
    descriptor = "MiB";
  }
  return `${bytes.toLocaleString()} ${descriptor}`;
}

export default function Files({ colorMode, prefix }) {
  const [loading, setLoading] = React.useState(true);
  const [files, setFiles] = React.useState([]);
  const [previewKey, setPreviewKey] = React.useState("");
  const navigate = useNavigate();

  React.useEffect(() => {
    // We utilize the "protected" level as a hack to access different prefixes
    // in the S3 bucket. All access is protected via IAM using the Cognito Identity,
    // so it doesn't follow the normal Amplify library pattern.
    Storage.configure({
      customPrefix: {
        protected: prefix,
      },
    });
    Storage.list("", { pageSize: "ALL", level: "protected" })
      .then((result) => {
        result.results = result.results.filter(e => !e.key.endsWith("user_info.py"));
        result.results.sort((a, b) => b.key.localeCompare(a.key));
        if (prefix !== "private/") {
          const groups = Array.from(
            new Set(result.results.map((e) => e.key.split("/")[0])).values()
          ).sort();
          result.results.forEach(
            (e) => (e["group"] = groups.indexOf(e.key.split("/")[0]))
          );
        }
        setFiles(result.results);
        setLoading(false);
      })
      .catch((err) => console.log(err));
  }, [prefix]);

  const { items, collectionProps } = useCollection(files, {
    sorting: {},
  });

  const downloadFile = (key) => {
    Storage.get(key, { level: "protected" })
      .then((result) => {
        window.open(result, "_blank");
      })
      .catch((err) => console.log(err));
  };

  const definitions = [];
  if (prefix !== "private/" && prefix !== "processing/") {
    definitions.push({
      id: "group",
      header: "Group",
      cell: (e) => e.group,
      sortingField: "group",
    });
  }
  definitions.push(
    {
      id: "key",
      header: "Name",
      cell: (e) =>
        prefix === "private/" || prefix === "processing/"
          ? e.key
          : e.key.split("/").splice(1).join("/"),
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
      cell: (e) => formatBytes(e.size),
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
    }
  );

  return (
    <>
      <Preview
        objectKey={previewKey}
        setObjectKey={setPreviewKey}
        colorMode={colorMode}
        spliceName={prefix !== "private/" && prefix !== "processing/"}
      />
      <Table
        items={items}
        {...collectionProps}
        columnDefinitions={definitions}
        loading={loading}
        loadingText="Loading"
        variant="embedded"
        trackBy="key"
        empty={
          <Box textAlign="center" color="inherit">
            <b>No submissions</b>
            <Box padding={{ bottom: "s" }} variant="p" color="inherit">
              Nothing has been uploaded yet
            </Box>
            <Button onClick={() => navigate("/submit")}>
              Upload submission
            </Button>
          </Box>
        }
      />
    </>
  );
}
