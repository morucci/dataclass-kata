#!/usr/bin/env python

from typing import Dict, List, Optional
import requests
import argparse

from dataclasses import dataclass, asdict
from dacite import from_dict


@dataclass
class BuildsetRef:
    """A Zuul's Build's Buildset Ref"""

    uuid: str


@dataclass
class BuildArtifactMetadata:
    """A Zuul Build's Artifact Metadata."""

    type: str


@dataclass
class BuildArtifact:
    """A Zuul Build's Artifact."""

    name: str
    url: str
    metadata: Optional[BuildArtifactMetadata]

    def __repr__(self):
        return "{name}: {url}".format(**asdict(self))


@dataclass
class Build:
    """A Zuul Build."""

    uuid: str
    job_name: str
    result: str
    start_time: str
    end_time: str
    duration: float
    voting: bool
    log_url: str
    node_name: Optional[str]
    error_detail: Optional[str]
    artifacts: List[BuildArtifact]
    provides: List
    project: str
    branch: str
    pipeline: str
    change: int
    patchset: str
    ref: str
    newrev: Optional[str]
    ref_url: str
    event_id: str
    buildset: BuildsetRef

    def format_artifacts(self):
        return "\n".join([str(artifact) for artifact in self.artifacts])

    def __repr__(self):
        return (
            (
                "Build {uuid} on {project}:{change},{patchset} (duration: {duration}"
                + " second(s)) finished with status: {result}"
            ).format(**asdict(self))
            + "\nArtifacts:\n"
            + self.format_artifacts()
        )


def get_build(api_url: str, tenant: str, uid: str) -> Dict:
    url = api_url + "/" + tenant + "/build/" + uid
    return requests.get(url).json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display a Zuul build")
    parser.add_argument(
        "--api-url",
        default="https://softwarefactory-project.io/zuul/api/tenant",
        help="The Zuul base API url",
    )
    parser.add_argument("--tenant", default="local", help="The tenant name")
    parser.add_argument("--id", required=True, help="The build id")

    args = parser.parse_args()

    build = from_dict(
        data_class=Build, data=get_build(args.api_url, args.tenant, args.id)
    )
    print(build)
