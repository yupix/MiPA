# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.1.0] 2022-12-24

### Added

- ✨ feat: add .flake8 config.
- ✨ feat: To be able to capture notes.
- ✨ added event `on_note_deleted`.
- ✨ added event `on_reacted`.
- ✨ added event `on_unreacted`.
- ✨ added `router` property a `Client` class attributes.
    - 💡 Direct instantiation of the `Router` class is deprecated.
- [@omg-xtao](https://github.com/omg-xtao) ✨ feat: added `hybridTimeline` channel [#9](https://github.com/yupix/MiPA/pull/9).


### Changed

- ⬆️ feat(deps): update mipac update mipac version.
- ✨ chore: Changed `parse_` lineage functions to asynchronous.
- 💥 feat: **BREAKING CHANGE** Change event name `on_message` from `on_note`.
- 💥 feat: **BREAKING CHANGE** Required Python version is 3.11.

### Fixed

- 🐛 fix: not working command Framework.
- 🐛 fix: Chat related stuff is flowing `on_message`.
    - 💡 Please use `on_chat` in the future!
