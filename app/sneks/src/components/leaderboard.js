import * as React from "react";
import Table from "@cloudscape-design/components/table";
import Box from "@cloudscape-design/components/box";
import { useCollection } from "@cloudscape-design/collection-hooks";

export default function Leaderboard({ scores, colors }) {
  const { items, collectionProps } = useCollection(scores, {
    sorting: {},
  });

  const definitions = [
    {
      id: "color",
      header: "Color",
      cell: (e) => (
        <div style={{ backgroundColor: `rgb(${colors[e.name]})` }}>&nbsp;</div>
      ),
      sortingField: "color",
    },
    {
      id: "name",
      header: "Name",
      cell: (e) => e.name.split("-").splice(6),
      sortingField: "name",
    },
    {
      id: "age",
      header: "Age",
      cell: (e) => e.age,
      sortingField: "age",
    },
    {
      id: "length",
      header: "Length",
      cell: (e) => e.length,
      sortingField: "length",
    },
    {
      id: "ended",
      header: "Ended",
      cell: (e) => e.ended,
      sortingField: "ended",
    },
    {
      id: "age1",
      header: "Age'",
      cell: (e) => e.age1,
      sortingField: "age1",
    },
    {
      id: "length1",
      header: "Length'",
      cell: (e) => e.length1,
      sortingField: "length1",
    },
    {
      id: "ended1",
      header: "Ended'",
      cell: (e) => e.ended1,
      sortingField: "ended1",
    },
  ];

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
    />
  );
}
