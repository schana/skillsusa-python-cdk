import * as React from "react";

export default function HomeHelp() {
  return (
    <div>
      <p>
        Sneks are scored and recorded shortly after submission and made
        available to see here.
      </p>
      <p>
        Scoring is composed of three components:
        <ol>
          <li>Age</li>
          <ul>
            <li>How many turns the Snek survives</li>
          </ul>
          <li>Length</li>
          <ul>
            <li>How many times the Snek consumes a food</li>
          </ul>
          <li>Ended</li>
          <ul>
            <li>How many other Sneks are ended by the Snek</li>
          </ul>
        </ol>
        For each evaluation of the Sneks, the scoring components are min-max
        normalized. The sum of the normalized scores is the value used to rank
        the Snek submissions.
      </p>
    </div>
  );
}
