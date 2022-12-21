import * as React from "react";
import Modal from "@cloudscape-design/components/modal";
import Box from "@cloudscape-design/components/box";
import Button from "@cloudscape-design/components/button";
import SpaceBetween from "@cloudscape-design/components/space-between";
import ProgressBar from "@cloudscape-design/components/progress-bar";
import { Storage } from "aws-amplify";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import python from "react-syntax-highlighter/dist/esm/languages/hljs/python";
import {
  a11yLight,
  a11yDark,
} from "react-syntax-highlighter/dist/esm/styles/hljs";

SyntaxHighlighter.registerLanguage("python", python);

export default function Preview({
  objectKey,
  setObjectKey,
  colorMode,
  spliceName,
}) {
  const [visible, setVisible] = React.useState(false);
  const [progress, setProgress] = React.useState(0);
  const [previewText, setPreviewText] = React.useState("");

  React.useEffect(() => {
    if (objectKey) {
      setVisible(true);
      Storage.get(objectKey, {
        download: true,
        progressCallback: (p) => {
          setProgress((100 * p.loaded) / p.total);
        },
        level: "protected",
      })
        .then((result) => {
          result.Body.text().then((data) => setPreviewText(data));
        })
        .catch((err) => console.log(err));
    } else {
      setVisible(false);
    }
  }, [objectKey]);

  return (
    <Modal
      size="max"
      onDismiss={() => setObjectKey("")}
      visible={visible}
      closeAriaLabel="Close modal"
      footer={
        <Box float="right">
          <SpaceBetween direction="horizontal" size="xs">
            <Button variant="link" onClick={() => setObjectKey("")}>
              Cancel
            </Button>
            <Button variant="primary" onClick={() => setObjectKey("")}>
              Done
            </Button>
          </SpaceBetween>
        </Box>
      }
      header={spliceName ? objectKey.split("/").splice(1) : objectKey}
    >
      <Box display={progress < 100 ? "" : "none"}>
        <ProgressBar value={progress} label="Preparing" />
      </Box>
      <SyntaxHighlighter
        language="python"
        style={colorMode === "light" ? a11yLight : a11yDark}
        showLineNumbers="true"
        wrapLongLines="true"
      >
        {previewText}# Your description should go here foo = bar()
      </SyntaxHighlighter>
    </Modal>
  );
}
