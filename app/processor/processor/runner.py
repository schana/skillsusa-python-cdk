import datetime
import pathlib
from collections import namedtuple

from sneks.config.config import config
from sneks.engine import runner


Score = namedtuple(
    "Score", ["name", "age", "length", "ended", "age1", "length1", "ended1"]
)


def run() -> (list[str], list[Score]):
    get_snake_submissions()
    copy_submissions_to_tmp()
    run_recordings()
    videos: list[str] = save_videos()
    scores: list[Score] = run_scoring()
    return videos, scores


def get_snake_submissions():
    pass


def copy_submissions_to_tmp():
    pass


def run_recordings() -> None:
    config.runs = 10
    config.graphics.display = True
    config.graphics.headless = True
    config.graphics.delay = 0
    config.graphics.record = True
    config.graphics.record_prefix = "/tmp/output"
    runner.main()


def run_scoring() -> list[Score]:
    config.turn_limit = 5000
    config.runs = 10
    config.graphics.display = False
    return [
        Score(
            name=s.raw.name,
            age=s.raw.age,
            length=s.raw.length,
            ended=s.raw.ended,
            age1=s.age,
            length1=s.length,
            ended1=s.ended,
        )
        for s in runner.main()
    ]


def save_videos() -> list[str]:
    prefix = pathlib.Path("/tmp/output/movies/")
    videos = prefix.glob("*.mp4")
    for video in videos:
        # TODO: do the s3 copy
        print(video)

    return [str(video.relative_to(prefix)) for video in videos]


def save_manifest(video_names: list[str], scores: list[Score]) -> None:
    structure = {
        "videos": [f"https://www.sneks.dev/games/{video}" for video in video_names],
        "scores": [
            score._asdict()
            for score in sorted(
                scores, key=lambda s: s.age1 + s.length1 + s.ended1, reverse=True
            )
        ],
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds"),
    }
    print(structure)

    # TODO:
    # manifest.json -> manifest_<timestamp>.json
    # new data -> manifest.json
