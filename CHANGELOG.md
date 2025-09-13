# CHANGELOG


## v1.5.3 (2025-09-13)

### Bug Fixes

- Bluetooth management socket communication on certain kernels
  ([#107](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/107),
  [`4e5e994`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/4e5e994e7b9f2bda7a26037fcbc114091d1d138c))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#94](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/94),
  [`10815e0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/10815e08ec975459bf75d85c69e0cc555f830758))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.5.2 (2025-05-21)

### Bug Fixes

- Update poetry to v2 ([#95](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/95),
  [`5902b0c`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/5902b0c5a9bcaae2db7c16964be88314f3952ba7))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#93](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/93),
  [`d8a9cc3`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/d8a9cc3d08b90d239411867655d6621fd378c63b))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.5.1 (2025-05-03)

### Bug Fixes

- Ensure public signature includes gone_silent
  ([#92](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/92),
  [`176502b`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/176502b2d5e64d798b9f7979df29f5007e18d561))


## v1.5.0 (2025-05-03)

### Chores

- Update dependabot.yml to include GHA
  ([`e942f61`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e942f61bb833dcadeeeb40f2b75f07510854fa0f))

- Update deps to fix CI
  ([#91](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/91),
  [`8d45f38`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/8d45f380a0e9b096c106a7039396e487ff67fdce))

- **deps**: Bump jinja2 from 3.1.5 to 3.1.6
  ([#84](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/84),
  [`ef86b2e`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/ef86b2eea4300a0363420a5d871ec0b5850692b2))

- **deps-ci**: Bump the github-actions group with 8 updates
  ([#90](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/90),
  [`1c99b89`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/1c99b895c1dbeee550f06a0a44cbe1a90b46887b))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: J. Nick Koston <nick@koston.org>

- **deps-dev**: Bump pytest from 8.3.4 to 8.3.5
  ([#82](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/82),
  [`e4988e8`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e4988e8af4dc5d21a61ea3f84768a3a48bcec2e8))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.4 to 8.3.5. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.4...8.3.5)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-asyncio from 0.25.3 to 0.26.0
  ([#85](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/85),
  [`a05b39a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/a05b39af200ae8f207ed8ac739a019d9024b4fbe))

Bumps [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) from 0.25.3 to 0.26.0. -
  [Release notes](https://github.com/pytest-dev/pytest-asyncio/releases) -
  [Commits](https://github.com/pytest-dev/pytest-asyncio/compare/v0.25.3...v0.26.0)

--- updated-dependencies: - dependency-name: pytest-asyncio dependency-version: 0.26.0

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-cov from 6.0.0 to 6.1.1
  ([#87](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/87),
  [`26ddaf4`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/26ddaf4fb6464be27558d3343dedbcdfb34cbd64))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#81](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/81),
  [`5ba466a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/5ba466a21fd7ed63e35095bff1d49789022810bd))

updates: - [github.com/commitizen-tools/commitizen: v4.2.1 →
  v4.4.1](https://github.com/commitizen-tools/commitizen/compare/v4.2.1...v4.4.1) -
  [github.com/PyCQA/isort: 6.0.0 → 6.0.1](https://github.com/PyCQA/isort/compare/6.0.0...6.0.1) -
  [github.com/PyCQA/flake8: 7.1.2 → 7.2.0](https://github.com/PyCQA/flake8/compare/7.1.2...7.2.0)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#86](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/86),
  [`c3f76f8`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c3f76f877511e0adbbb92da03cee7d9cefdfdc34))

updates: - [github.com/commitizen-tools/commitizen: v4.4.1 →
  v4.5.0](https://github.com/commitizen-tools/commitizen/compare/v4.4.1...v4.5.0)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#88](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/88),
  [`c7a1de1`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c7a1de10f3932c8f0f3acb84109bf5a45c152e03))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Try USB reset if the adapter has gone silent
  ([#89](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/89),
  [`c615af1`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c615af120941a1d38fc082f4eab2597c55c3f4d2))


## v1.4.5 (2025-03-13)

### Bug Fixes

- Downgrade power on success log message to debug
  ([#83](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/83),
  [`da6ca83`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/da6ca83c1c55b4c154b46b18afacbf3ab7d9b063))


## v1.4.4 (2025-02-19)

### Bug Fixes

- Handle case where adapter moves to index 0 after USB reset
  ([#79](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/79),
  [`34517d3`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/34517d37e426cba26cceb0bcdc8da2f98e63610b))


## v1.4.3 (2025-02-19)

### Bug Fixes

- Rfkill unblocking when adapter idx is 0
  ([#78](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/78),
  [`f6dbba0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/f6dbba060307aca0657ce6a967153c2e373b6aaa))

### Chores

- Create dependabot.yml
  ([`e412f97`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e412f97b02cdf64be5cad1347d5ec68eac1a6fb4))

- **deps**: Bump aiohttp from 3.9.5 to 3.10.11
  ([#67](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/67),
  [`95b906e`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/95b906e26681e488043d33dd7b6630a792f5d4ee))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump async-timeout from 4.0.3 to 5.0.1
  ([#68](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/68),
  [`7bd0f38`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7bd0f3852b394b9ec0909fb7e615a353c48e577e))

- **deps**: Bump certifi from 2024.6.2 to 2024.7.4
  ([#65](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/65),
  [`a9ba476`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/a9ba476e51ba0aee227a8a50cae8d49a45e698af))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump jinja2 from 3.1.4 to 3.1.5
  ([#64](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/64),
  [`65f2b3d`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/65f2b3da77fa70927b4737dfa8a11d1aa21cec0c))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump myst-parser from 0.18.1 to 1.0.0
  ([#61](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/61),
  [`8f2c913`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/8f2c91376ca173a41403a68a5b8fe290cc4823ba))

Bumps [myst-parser](https://github.com/executablebooks/MyST-Parser) from 0.18.1 to 1.0.0. - [Release
  notes](https://github.com/executablebooks/MyST-Parser/releases) -
  [Changelog](https://github.com/executablebooks/MyST-Parser/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/executablebooks/MyST-Parser/compare/v0.18.1...v1.0.0)

--- updated-dependencies: - dependency-name: myst-parser dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump myst-parser from 1.0.0 to 3.0.1
  ([#72](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/72),
  [`6dfd5ac`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/6dfd5acffeabcda0e465d23ea63855c46cedf038))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx from 5.3.0 to 6.2.1
  ([#69](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/69),
  [`7442426`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7442426226bf7bb07b9d57890aed55f778c2362f))

- **deps**: Bump sphinx from 6.2.1 to 7.4.7
  ([#75](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/75),
  [`c34f36b`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c34f36bc83edef560930d610f6e66192a832561f))

- **deps**: Bump sphinx-rtd-theme from 1.3.0 to 2.0.0
  ([#60](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/60),
  [`9e29600`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/9e296002f07bc99424a6f5b0fd80507cbf350e81))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx-rtd-theme from 2.0.0 to 3.0.2
  ([#71](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/71),
  [`7678868`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7678868d956b92c8cd75296692b1684d8f69017e))

- **deps-dev**: Bump pytest from 7.4.4 to 8.3.4
  ([#59](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/59),
  [`caa4b28`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/caa4b2894db891105fc398a1bf4eac4871c3c71c))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-asyncio from 0.23.7 to 0.25.2
  ([#66](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/66),
  [`f06eb67`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/f06eb67bba4d1ed172034fc8873419ecbaec578e))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-asyncio from 0.25.2 to 0.25.3
  ([#74](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/74),
  [`b216503`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/b21650347fbe316002fe1e18f84cb5755173a99e))

- **deps-dev**: Bump pytest-cov from 3.0.0 to 6.0.0
  ([#63](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/63),
  [`69ceaa5`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/69ceaa579c6880fb9921124ec9d470f2eb724c93))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#47](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/47),
  [`e25b028`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e25b0288577fa4ab4ca3cc57d64787e27bdf3489))

* chore(pre-commit.ci): pre-commit autoupdate

updates: - [github.com/commitizen-tools/commitizen: v2.31.0 →
  v3.27.0](https://github.com/commitizen-tools/commitizen/compare/v2.31.0...v3.27.0) -
  [github.com/pre-commit/pre-commit-hooks: v4.3.0 →
  v4.6.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.3.0...v4.6.0) -
  [github.com/pre-commit/mirrors-prettier: v2.7.1 →
  v4.0.0-alpha.8](https://github.com/pre-commit/mirrors-prettier/compare/v2.7.1...v4.0.0-alpha.8) -
  [github.com/asottile/pyupgrade: v2.37.3 →
  v3.16.0](https://github.com/asottile/pyupgrade/compare/v2.37.3...v3.16.0) -
  [github.com/PyCQA/isort: 5.12.0 → 5.13.2](https://github.com/PyCQA/isort/compare/5.12.0...5.13.2)
  - [github.com/psf/black: 22.6.0 → 24.4.2](https://github.com/psf/black/compare/22.6.0...24.4.2) -
  [github.com/codespell-project/codespell: v2.2.1 →
  v2.3.0](https://github.com/codespell-project/codespell/compare/v2.2.1...v2.3.0) -
  [github.com/PyCQA/flake8: 5.0.4 → 7.1.0](https://github.com/PyCQA/flake8/compare/5.0.4...7.1.0) -
  [github.com/pre-commit/mirrors-mypy: v0.931 →
  v1.10.1](https://github.com/pre-commit/mirrors-mypy/compare/v0.931...v1.10.1) -
  [github.com/PyCQA/bandit: 1.7.4 → 1.7.9](https://github.com/PyCQA/bandit/compare/1.7.4...1.7.9)

* chore(pre-commit.ci): auto fixes

* fix: lint

---------

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

Co-authored-by: J. Nick Koston <nick@koston.org>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#48](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/48),
  [`15d2101`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/15d2101864699b2ab8d694298b2b2626422e7c95))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#49](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/49),
  [`f54eccd`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/f54eccdf3638b1ce070dd822491156b9179bb908))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#50](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/50),
  [`d04be3e`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/d04be3e25f87df77075d6a4ae09f6bec1604a3eb))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#51](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/51),
  [`a0bbc33`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/a0bbc33a5e1d0bd2fdee57344615c37f68dca1bf))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#52](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/52),
  [`59ecbda`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/59ecbdaae20dad595f70dc45bdb428e2904eded6))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#53](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/53),
  [`c9319c6`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c9319c6f9c1a5691437057a5d856bca9e64622f9))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

Co-authored-by: J. Nick Koston <nick@koston.org>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#54](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/54),
  [`2263e37`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/2263e3706559bc3052a1377571079a08d05f75ce))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#57](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/57),
  [`0e9084a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0e9084a152b802060a1e869b1f3cf2e74952028a))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#58](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/58),
  [`b369f20`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/b369f20fe8bd608645806495af02d43fea51d64e))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#70](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/70),
  [`eef87a0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/eef87a05c749aca5c367629c21b76141dc472ca9))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#73](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/73),
  [`db65606`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/db656061f7de78635d8aa81224c3d9dd4b91de9f))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#76](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/76),
  [`e0d8d14`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e0d8d143ad032d648ac71e371e4cf18b4580e3a1))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#77](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/77),
  [`d87450a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/d87450a3799f9164f67f5663296f26b945395b99))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.4.2 (2024-04-25)

### Bug Fixes

- Ensure timeout does not raise cancellation
  ([#46](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/46),
  [`4575fdd`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/4575fdd52778e09dee5e6bce51e7636e9609aaac))


## v1.4.1 (2024-04-18)

### Bug Fixes

- Wait for connection made
  ([#45](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/45),
  [`70aa8df`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/70aa8df23ac7a604177af680b63fdb1f00e430b8))


## v1.4.0 (2024-03-13)

### Features

- Only import recovery code the first time the recovery is called
  ([#44](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/44),
  [`39372f0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/39372f085e624a7fba8d06ed1ddc8a4a52c7bb7c))


## v1.3.0 (2024-01-10)

### Features

- Ensure library can be loaded on windows
  ([#43](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/43),
  [`dd234f8`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/dd234f847c54fe8471b51378ab03b2d1a9f2f497))


## v1.2.3 (2023-09-09)

### Bug Fixes

- Add missing async keyword to send timeout
  ([#42](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/42),
  [`1097e44`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/1097e44a8c6051aeb6e9f4d53631c8ecf1e47d54))


## v1.2.2 (2023-09-07)

### Bug Fixes

- Ensure timeouts work with py3.11
  ([#41](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/41),
  [`99b9f48`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/99b9f48f8f742d6004720b26e25b9c1f6cd455e7))


## v1.2.1 (2023-07-12)

### Bug Fixes

- Make MGMTBluetoothCtl aware of down adapters
  ([#38](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/38),
  [`3c6bc12`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/3c6bc12e021611590e13c400aeedc665b582a9c3))

### Chores

- Fix ci ([#37](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/37),
  [`68b45f4`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/68b45f493a0ec67c11b055498a8208fc08fd640a))

- Fix ci ([#39](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/39),
  [`9f72572`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/9f725728223cb32af868429f9c2b35ecf22c068d))


## v1.2.0 (2023-05-10)

### Features

- Try to bounce the adapter if setting power state fails
  ([#36](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/36),
  [`11ec5e2`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/11ec5e2e5b8fc8e6d58d9b822dc333dbf89e6952))


## v1.1.2 (2023-05-04)

### Bug Fixes

- Proceed with reset when getting power state times out
  ([#34](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/34),
  [`aae8c84`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/aae8c848fb894686ba1076d395b402701b0cedc5))


## v1.1.1 (2023-05-03)

### Bug Fixes

- Pass on event types we do not know how to process
  ([#33](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/33),
  [`2bbca73`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/2bbca73867f6bbd599544fe47ff6b0c468c6436a))


## v1.1.0 (2023-05-03)

### Chores

- Fix ci ([#32](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/32),
  [`9445c54`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/9445c54fb1663aa4c2b308d51b6ff5035f0589ee))

### Features

- Do a down/up on the interface when resetting the adapter
  ([#31](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/31),
  [`ae3f63b`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/ae3f63b0b13672df6375e4c6ee5514439484a31f))


## v1.0.3 (2022-12-15)

### Bug Fixes

- Handle the btsocket being closed out from under us
  ([#29](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/29),
  [`1e0d878`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/1e0d87853379e1ca89b50ecd9698e8c61c37e398))

### Chores

- Add python 3.11 to the ci
  ([#30](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/30),
  [`7174b10`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7174b1008d727a5658a1d0c9e4c3fadfdeccc9cd))


## v1.0.2 (2022-12-15)

### Bug Fixes

- Handle the case where a btsocket cannot be created
  ([#28](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/28),
  [`6e8e8e1`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/6e8e8e1b0b42a0c830a70cafafd8a25e3df631d5))


## v1.0.1 (2022-12-15)

### Bug Fixes

- Handle adapter moving to a new hci number after reset
  ([#27](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/27),
  [`662f710`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/662f710c30b07a0904cc9a3d00b39303ee43db4a))


## v1.0.0 (2022-12-12)

### Features

- Add support for being able to reset the adapter by mac address when the hci interface is lost
  ([#26](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/26),
  [`72d6114`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/72d6114a4c6b553fb574f43fc793fd0c7a969521))

BREAKING CHANGE: The mac address must now be passed to `recover_adapter`

- Do not check for the BTLE bit since it can be missing when failed: If the adapter was fully
  unresponsive the BTLE bit may be missing so we should still try to reset the adapter anyways since
  we already know they managed to set it up. - Try to lookup the adapter by mac address since the
  hci interface may have disappeared and we can't reset an adapter we can no longer find.

### Breaking Changes

- The mac address must now be passed to `recover_adapter`


## v0.5.5 (2022-12-09)

### Bug Fixes

- Handle BluetoothSocketError and fallback to usb reset
  ([#25](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/25),
  [`5d6d1c3`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/5d6d1c390279fbe712f6330f8997dc87f981d5e7))


## v0.5.4 (2022-12-02)

### Bug Fixes

- Downgrade permission denied error logging when attempting usb reset
  ([#24](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/24),
  [`79cf457`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/79cf457f38071ba8265864c8b18acda184065f97))


## v0.5.3 (2022-11-29)

### Bug Fixes

- For rfkill not being readable
  ([#23](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/23),
  [`6c168a0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/6c168a0704401d6dfcd95ade31b2df47cee03060))


## v0.5.2 (2022-11-27)

### Bug Fixes

- Ensure dbus wait always happens on success case
  ([#22](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/22),
  [`df8e7e0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/df8e7e0647dd63aa173d8e815b6a5cbfaf40ff41))


## v0.5.1 (2022-11-27)

### Bug Fixes

- Bump usb-devices ([#21](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/21),
  [`06c2d05`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/06c2d05f530965fee9a7ea7d0cf3596ba65bddfe))


## v0.5.0 (2022-11-27)

### Features

- Implement generic usb reset
  ([#20](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/20),
  [`0d7f045`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0d7f045703b192b0aa86de482d128a43f48e84bf))


## v0.4.0 (2022-11-16)

### Features

- Reduce overhead to find a response
  ([#18](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/18),
  [`219d3f7`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/219d3f77d20415c22412872a24896adee8eefb8e))


## v0.3.6 (2022-10-19)

### Bug Fixes

- Soft_block and hard_block were unbound when rfkill fails
  ([#15](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/15),
  [`9d2aa1a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/9d2aa1a5245ceef07ecb0f1cbdf668782ff5ec81))


## v0.3.5 (2022-10-19)

### Bug Fixes

- Missing param in format string for rfkill timeout message
  ([#13](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/13),
  [`0022d8a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0022d8a28849f51abdc055e6cc1b3c19cbe6abdf))


## v0.3.4 (2022-10-10)

### Bug Fixes

- Ensure management socket is closed on failure to prevent a leak
  ([#12](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/12),
  [`4ab673f`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/4ab673fb989ae696327150337a4dfd4d1770ca9d))

I found this via dumb luck as I managed to knock a bluetooth adapter just out of the usb socket so
  it keeps disconnecting and reconnecting. Net results is a leak in python-btsocket which results in
  the bluetooth management socket not being closed if the stack doesn't respond so it leaves it open
  when it tries to reset it and leaks. Worse is the leak builds up over time if it happens again and
  if you have a busy systems its processing all the data while waiting for a response.

Make BluetoothMGMTProtocol a context manger and an asyncio.Protocol to ensure if anything goes wrong
  the underlying bluetooth management socket gets closed.


## v0.3.3 (2022-09-11)

### Bug Fixes

- Downgrade rfkill check logging to debug
  ([#11](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/11),
  [`80471e6`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/80471e6155d9d72a2ffa467d580aec4315968aaf))


## v0.3.2 (2022-09-08)

### Bug Fixes

- Downgrade rfkill check logging to debug
  ([#10](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/10),
  [`c7b9539`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c7b95396c78e9d05a78ce1b9022c481f30a2b9e0))


## v0.3.1 (2022-09-06)

### Bug Fixes

- Handle invalid data in rfkill
  ([#9](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/9),
  [`31c1480`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/31c148013721b22f01d9a107d01a6d6cc576c815))


## v0.3.0 (2022-08-30)

### Features

- Handle no permission to check rfkill
  ([#8](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/8),
  [`fcda90d`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/fcda90dcdd104608fb2db4b9feca90a7b0e5c8d5))


## v0.2.2 (2022-08-20)

### Bug Fixes

- Give Dbus a bit more time to catch up if the adapter has been recovered
  ([#7](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/7),
  [`216ef1f`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/216ef1fd0e9ec4ed3b022f9f194282d7b2b359cf))


## v0.2.1 (2022-08-20)

### Bug Fixes

- Handle libc.so.6 missing
  ([#6](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/6),
  [`0d9f4cb`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0d9f4cbc9bf2a422c2f7a889354b76cfe7c75620))

- Handle rfkill not being available in the container
  ([#5](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/5),
  [`7736c35`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7736c35279351c8877514f3324f7428447bdaaea))


## v0.2.0 (2022-08-20)

### Features

- Give DBus some time to catch up to avoid spurious warnings
  ([#4](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/4),
  [`63188f6`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/63188f694b667ce5418736f5ca02db8484bc83b9))


## v0.1.0 (2022-08-19)

### Chores

- Initial commit
  ([`3b0adee`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/3b0adee4377dc2c52dbb8439fbaadec457af725f))

### Features

- First release ([#3](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/3),
  [`0109dde`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0109dde7631e6c4e0b96733e37be8a98beae1822))

- Init repo ([#1](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/1),
  [`c82627f`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c82627f75d78d41550e3e37a9e9a9ed35feec466))

- Port reset_bluetooth to asyncio
  ([#2](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/pull/2),
  [`e7ef901`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/e7ef901017f34e57b8111004889c4b4891fb8515))
