# Picto performance evaluation

This repository contains the required artefacts for replicating the performance evaluation used to validate the lazy evaluation capabilities provided by the Picto tool. This evaluation compares two transformation approaches for generating HTML model views, namely:

- A batch model-to-text (M2T) transformation generation with general purpose methods (EGL).
- A lazy generation of model views through the use of the Picto plugin.

The evaluation has been tested in a Ubuntu 18.04 machine running dot version 2.40.1.

## Installation / Configuration

The following programs are required:

- Java JDK 11
- A [Graphviz](https://www.graphviz.org/download/) installation, as the generated views are represented in the dot format. On Windows, it might be necessary to add the `dot.exe` to the environment variables of the system. On Mac and Linux, the `dot` command is called from its typical installation location, e.g., `/usr/local/bin/dot` and `/usr/bin/dot` respectively.

### Eclipse

The tests have been carried out using an Eclipse 2021-12 installation with support for setting a [target platform](https://www.vogella.com/tutorials/EclipseTargetPlatform/article.html). You can get such an eclipse installation by using Epsilon's own [eclipse installer](https://www.eclipse.org/epsilon/download/).

The tests use a modified version of the Epsilon model management suite source projects, including some special modifications for the profiling of Picto views generation. The next steps allow obtaining this environment and importing all the profiling projects:

1. Checkout into your system the following git repository: https://doi.org/10.5281/zenodo.7712752
2. In an Eclipse workspace, import all projects under the `plugins` and `releng` folders of the previous repository.
3. There is an [Eclipse Target Platform](https://www.vogella.com/tutorials/EclipseTargetPlatform/article.html) at `org.eclipse.epsilon.target/org.eclipse.epsilon.target.target`. Load this target platform by opening it and clicking on *Set as Active Target Platform*.
4. Run a *second* Eclipse instance from this initial workspace. To do that, right-click on any of the imported Eclipse projects, and select *Run as > Eclipse Application*.
5. In the second Eclipse instance, import the `org.eclipse.epsilon.picto.profiling` project contained in this repository. All tests will be run from this Eclipse instance.

### Plotting the results

Some Python scripts are provided to generate the graph figures of the paper. These scripts use Pandas and Matplotlib, and require a **Python 3 environment** with the following packages:

- `pandas`
- `numpy`
- `matplotlib`

The authors used an [Anaconda 3](https://www.anaconda.com/products/individual) installation, which by default contains the enumerated packages.

In addition, the plot scripts use Latex fonts for a better alignment with the manuscript style. So, a **Latex installation** is also required, with the `libertine` package installed.

## Run Standalone Java M2T Transformations

These transformations are started by executing two simple java programs. We recommend running each program in isolation, as the standalone transformations include parallel execution in one of their versions. From the second eclipse instance, do:

- Run `org.eclipse.epsilon.picto.profiling/src/org/eclipse/epsilon/picto/profiling/batchExecution/RenderEcore.java` as a Java application. When finished, the `batchRenderEcore.csv` and `batchRenderEcoreParallel.csv` CSV files would have been generated in the root of the project.
- Run `org.eclipse.epsilon.picto.profiling/src/org/eclipse/epsilon/picto/profiling/batchExecution/RenderGenComps.java` as a Java application. When finished, the `batchRenderGenComps.csv` and `batchRenderGenCompsParallel.csv` CSV files would have been generated in the root of the project.

Depending on the machine, each execution can be expected to take around 20-30 minutes.

## Run Picto Transformations

Before running these tests, we recommend to close all editors of the Eclipse instance (in case something was opened because of the previous transformations, for example).

- Make visible the `Picto` view. After clicking *Window > Show View > Other..* in the menu, an *Epsilon > Picto* view should be available. Make this window visible in the workspace.
- To calculate the times of a model, the following steps are required:
  - Double click in a model, and make sure the Picto window is visible.
  - A rendering progress widget would appear in the bottom right of the Picto, which means that the views are being generated and the times gathered.
  - Once the view of the model is shown, the measurements are complete, and a new csv file would be generated besides the opened model (for instance, if the opened model is `models/genComps/gencomps-12.9K.model`, a `models/genComps/gencomps-12.9K.model.profiling.csv` would be generated). Refresh the folder containing the model to see the new file.
  - Close the editor of the opened model.
- We recommend running the generations for each model one by one, again in isolation. The models that should be processed to at least generate the paper figures are:
  - `org.eclipse.epsilon.picto.profiling/models/ecore`
    - `UML.ecore`
    - `CIM15.ecore`
    - `GluemodelEmoflonTTC2017.ecore`
    - `RevEngSirius.ecore`
  - `org.eclipse.epsilon.picto.profiling/models/gencomps`
    - `gencomps-12.9K.model`
    - `gencomps-29K.model`

## (Optional) Plotting the results

Once the standalone M2T transformation and all individual picto rendering measurements have been taken, different scripts from the `plotscripts` folder can be ran to obtain plots. We detail the required steps to create the two plots shown in the paper. The execution of the python scripts might vary depending on your system. We provide instructions to run these scripts from a terminal and from the `plotscripts` folder.

### Ecore models

From `org.eclipse.epsilon.picto.profiling/plotscripts`, run:

`python final_Ecore_4squared_plot.py`

The `renderEcoreSquared.pdf` file would be generated in the root of the `org.eclipse.epsilon.picto.profiling` eclipse project, as well as a `renderEcoreSquared-data.txt` data with relevant information that was used when comparing and discussing the approaches in the paper.

### GenComps models

From `org.eclipse.epsilon.picto.profiling/plotscripts`, run:

`python final_gencomps_4squared_plot.py`

The `renderGenCompsSquared.pdf` file would be generated in the root of the eclipse project, as well as a `renderGenCompsSquared-data.txt` data with relevant information that was used when comparing and discussing the approaches in the paper.
