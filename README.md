# aoc-rms

This project is a collection of RMS-related utilities, to be used in conjunction with one another, or alongside other tools. Broadly speaking, the goal is to interpret aspects of each RMS, and provide a basis for comparison. Furthermore, it serves as a curated collection of RMS files.

## Utilities

- `metadata`: Extract metadata from the file and filename.
- `diff`: Compute similarities/differences between two RMS files.
- `cluster`: Group RMS files based on similarity.
- `parse`: Implementation of RMS [grammar](https://en.wikipedia.org/wiki/Formal_grammar).

## Packs

- `SYNC2014`: Nations Cup I
- `SYNC2015`: Nations Cup II
- `SYNC2017`: Nations Cup III
- `WSVG`: Word Series of Video Games
- `WiC`: War is Coming
- `BOP`: Balance of Power
- `EGC`: Every Game Counts #1: Strike the Balance
- `ES`: Ensemble Studios supplement

## Development

Contributions are welcome. Fork and submit a pull request. Please add or update tests if your submission includes code. All commits must pass `tox`.
