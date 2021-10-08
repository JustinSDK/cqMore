# cqMore

cqMore is a [CadQuery](https://github.com/CadQuery/cadquery) plugin (under construction).

![cqMore](images/ripple.JPG)

## Installation

Please use `conda` to install CadQuery and its dependencies (see [Getting started](https://github.com/CadQuery/cadquery#getting-started) of CadQuery). Then, use `conda` to install `git` if you don't have it:

	conda install git
	
To install cqMore directly from GitHub, run the following `pip` command:

	pip install git+git://github.com/JustinSDK/cqMore.git

## Introduction

You may simply use `cqMore.Workplane` to replace `cadquery.Workplane`. For example:

    from cqMore import Workplane

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

You may also attach methods of `cqMore.Workplane` to `cadquery.Workplane`, such as:

    from cadquery import Workplane
    import cqMore

    Workplane.makePolygon = cqMore.Workplane.makePolygon

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

## API Reference

- [`cqMore.Workplane`](docs/workplane.md)
