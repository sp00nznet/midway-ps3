# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Build scaffold on the shared ps3recomp runtime: `CMakeLists.txt`, `build.py`,
  `tools/relift.sh`.
- The two SPURS render jobs are cut from the EBOOT's `.data` and lifted by
  `relift.sh`.
- Boots past the logo movies to the title screen, carousel and an emulated
  arcade game (Vindicators Part II attract loop).
- Docs: progress log.

### Fixed

- Draws no longer drop at PSO build: `cellSpursJoinJobChain` waits for the
  chain (ps3recomp #185).
- The game no longer waits forever after booting the movie player: `cellSail`
  reports player state changes (ps3recomp #190).
