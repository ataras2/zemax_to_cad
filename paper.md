---
title: 'Zemax to CAD: Scripting for optomechanical design'
tags:
  - Python
  - Zemax 
  - Solidworks
  - Optomechanical design
  - Instrumentation
authors:
  - name: Adam K. Taras
    orcid: 0000-0000-0000-0000
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
affiliations:
 - name: The University of Sydney
   index: 1
date: 30/10/2024
bibliography: paper.bib

---

# Summary



The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration).

# Statement of need

As astronomical instrumentation continues to grow, each generation of instruments is more complex than the last, with more demanding requirements imposed to meet science goals. It is increasingly important to have rapid feedback loops between different stages of a design. Existing software packages do one job well: Zemax allows optics engineers to optimize many optical elements to maximise performance and Solidworks (or similar CAD packages) enable mechanical engineers to turn sketches of optics into. These are by far the most common suites used. 

- Existing workflow description:

- There exist tutorials on how to interface Python with solidworks (e.g. https://mason-landry.hashnode.dev/automating-solidworks-using-python-492b15303db3) and on solidworks only (https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/J.-Harwell_SolidWorksTutorial.pdf), but having something tailored to the structure of instrumentation projects would greatly reduce the amount of scripting that mechanical engineers need to do. Also Zemax has its ZOS API, but this doesn't really provide a way of improving this design loop. 

I originally applied an early version `zemax2cad` to transform optical designs of the Heimdallr and Baldr instruments in the Asgard instrument suite [@CITATION to heim paper]. It is currently being used to finalise design of the Bifrost instrument [@cite]. The package is applicable to any instrumentation, however particularly 


`Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

Microsoft Copilot was used for the code but not this markdown file. 

# References