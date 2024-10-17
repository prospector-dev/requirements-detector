import semver


class VersionConstraint:
    def is_empty(self) -> bool:
        raise NotImplementedError()

    def is_any(self) -> bool:
        raise NotImplementedError()

    def allows(self, version: semver.Version) -> bool:
        raise NotImplementedError()

    def allows_all(self, other: "VersionConstraint") -> bool:
        raise NotImplementedError()

    def allows_any(self, other: "VersionConstraint") -> bool:
        raise NotImplementedError()

    def intersect(self, other: "VersionConstraint") -> "VersionConstraint":
        raise NotImplementedError()

    def union(self, other: "VersionConstraint") -> "VersionConstraint":
        raise NotImplementedError()

    def difference(self, other: "VersionConstraint") -> "VersionConstraint":
        raise NotImplementedError()
