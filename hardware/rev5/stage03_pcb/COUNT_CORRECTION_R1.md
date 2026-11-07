# Stage03R1 — physical via recount correction

Date: 2026-11-07

## Error found

The first Stage03 audit counted objects using the prefix token `(via`. The KiCad PCB file contains 21 physical top-level via blocks and four DRC-rule entries named `(vias not_allowed)`. The broad prefix parser counted both categories and reported 25.

## Correct method

Count only top-level physical blocks beginning with the exact token `\n\t(via\n`. The same check was run against the immutable source and the Stage03 candidate.

## Correct result

- Source: 21 physical vias.
- Stage03 candidate: 21 physical vias.
- Tracks: 207 / 207.
- Zones: 5 / 5.
- Board file SHA-256 unchanged: `ee73c41b8612b430947aaaffa848d30d5a6a46b0dfcfc78702200968f5eb1537`.

## Corrected artifact package

[Stage03R1 OneDrive folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgD9TMKIfuSgQa_O5KN5br94ATrWzH_ylvcmSph4diZcSJg)

[Stage03R1 complete ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQC7gkvDHw_XQpgaaWC95G_bAXE4XZnOtcgD5lZMVie5jjY)

The earlier Stage03 package has not been removed. Stage03R1 supersedes its audit/report metadata only. The PCB bytes remain identical.
