<!-- ---
title: 'Zemax to CAD: plug and play, agile optomechanical design'
tags:
  - Python
  - Zemax 
  - Solidworks
  - Optomechanical design
  - Instrumentation
authors:
  - name: Adam K. Taras
    orcid: 0000-0002-4558-2222
    affiliation: "1"
affiliations:
 - name: The University of Sydney
   index: 1
date: 30/10/2024
bibliography: paper.bib

--- -->

# Summary

<!-- The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration). -->

The design stage is a critical part of the development of instruments for astronomy, with time critical decisions for procurement and 

The contributions of this work are as follows:
 1. A lightweight, flexible, object oriented interface in python that enables interfaces with Zemax text, Excel, CSV, and Solidworks text files, as well as with the ZOS API. 
 2. Examples of use on realistic size projects, tailored to the typically low level of familiarity of physics students with Zemax and Solidworks. This is beyond example scripts and contains guides on how to use this whole framework in Solidworks.

# Statement of need

As astronomical instrumentation continues to grow, each generation of instruments is more complex than the last, with more demanding requirements imposed to meet science goals. It is increasingly important to have rapid feedback loops between different stages of a design. Existing software packages do one job well: Zemax allows optics engineers to optimize many optical elements to maximise performance and Solidworks (or similar CAD packages) enable mechanical engineers to turn sketches of optics into. These are by far the most common suites used. 

A typical workflow for an instrument would be as follows: First, high level requirements are written, driven by science cases. Tradeoff studies narrow this down to a conceptual sketch of the critical components. Once the project is more certain, optical design using ray tracing or similar software selects optics e.g. lenses, mirrors or prisms, and optimises the positions and parameters to best suit the task. The optomechanical constraints are roughly known but based off priors rather than this particular instrument. Next, the design is exported using the ray tracing tool to a CAD model. The format used must be universal (e.g. STEP files), however this comes at the cost of losing the correspondence between objects/surfaces in the optical design and the 3D model. This is then loaded into a CAD package where "mates" are made - constraints on how objects in the model must be oriented relative to each other. In the simplest case, a mechanical engineer must make the number of optics $N_{\rm optics}\sim\mathcal{O(10^2)}$ reference points on the exported model, $N_{\rm optics}$ reference points on the physical objects, and $N_{\rm optics}$ position mates (ignoring tilts). In a world where the project is designed once and works flawlessly this might be acceptable, however this is often the case. Furthermore, projects are shifting more towards flexible design practices, using agile methodology to deal with changing requirements. With this comes multiple iterations, and the complexity of this change from optical to 3D CAD models scales linearly as the number of iterations $N_{\rm iter}$, which be up to hundreds for large projects.

Instead, using `zemax_to_cad` gives users the ability to avoid these menial tasks, extract information in a more accesible form and interface different parts of the project together in a much more natural way. The typical workflow using this package would involve making $N_{\rm optics}$ point references on the model objects, running a python script, and generating a series of location mates (depending on geometry, this is either $2N_{\rm optics}$ or $3N_{\rm optics}$) that are linked to the output of this python script. Then, every time a change is made to the optical design, the script updates the mates of the 3D model. There is only a (small, $<1$ min) computational cost associated with this update, as opposed to human cost that scales with $N_{\rm optics}$ if using the conventional approach.

- There exist tutorials on how to interface Python with solidworks (e.g. https://mason-landry.hashnode.dev/automating-solidworks-using-python-492b15303db3) and on solidworks only (https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/J.-Harwell_SolidWorksTutorial.pdf), but having something tailored to the structure of instrumentation projects would greatly reduce the amount of scripting that mechanical engineers need to do. Also Zemax has its ZOS API, but this doesn't really provide a way of improving this design loop. 

I originally applied an early version `zemax2cad` to transform optical designs of the Heimdallr and Baldr instruments in the Asgard instrument suite [@CITATION to heim paper]. It is currently being used to finalise design of the Bifrost instrument [@cite]. The package is applicable to any instrumentation, however particularly useful for projects with multiple upgrades/phases, or instruments involved with multiple beams (typically for interferometry).

# Example use cases

## Getting out of Zemax
Now that you are happy with an optical design in Zemax, you want to validate that the otpomechanics work well. 

If, for whatever reason, the remote PC doesn't have python or is run by a different user, this step can also be completed manually using the "Save as" functionality in the perscription data tab.

 Using this package, run the `m_zos_to_test.py` script using the following:

```bash
python docs/examples/m_zos_to_test.py --config 1,2,3,4 --outfile my_prescription_data_c{config}.txt
```

This will create 4 new text files containing the prescription data, each with the configuration number. 

## Solidifying an optical design
Next, we use the rest of the package to reformat the text files from the previous step into a Solidworks format.

See the script in `docs/examples/m_convert_to_solidworks.py`. You will likely need to adjust the list of surfaces exported and the transformation of the surfaces. It is easiest if the resulting origin and coordinate system is aligned with a stable fiducial, such as the optical bench holding the whole setup. You are also able to select which degrees of freedom are exported.

Once the script is run, review the output file produced, verifying that all your surfaces have exported. In Solidworks go to (or search for) Equations, and select ???

## Using 3D geometry for downstream applications: move_image and move_pupil
Beyond a direct translation to a 3D model, the package can also be used for downstream tasks, typically involving small calculations using the data from the positions of key surfaces. 

One realisitc use case is that when a single beam has two motorised stages, changing the angles of the mirrors with respect to a nominal orientation in order to allow for adjustments of the physical system. With two motors in both tip and tilt, there are (subject to choices of motors locations) enough degrees of freedom to control both the position of the image and the position of the pupil. Understanding how to change from image/pupil position to mirror angle is useful for developing software that is effecient and usable.

We share an example from the Heimdallr instrument, which has a tip/tilt motor on the focusing mirror and on a mirror an the intermediate plane, with different distances for different beams (different configurations in zemax). `docs/examples/???` shows how to do the calculation using this package, even when the intermediate focal plane isn't an explicit surface in Zemax. 

This result can be used in both the design - to check that the motors have enough leverage to control the image and pupil within expected tolerances - and the deployment - to translate user commands of the form "move pupil of beam 1 up 0.5mm".

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