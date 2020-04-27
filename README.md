# models2020-picto-data

## Run Standalone Java M2T Transformations

- Requires an Eclispe installation with EGL, and the "dot" command in the user path.
- Import the "org.eclipse.epsilon.picto.profiling" project into a workspace.
- Run the desired "Render{}.java", such as "RenderGenComps.java"

## Run Picto Transformations

- Check out the "picto-profiling" branch of the Epsilon repo, and import the plugins related to Picto.
- Launch a new Eclipse instance from any of the plugins.
- In the launched workspace, import the "org.eclipse.epsilon.picto.profiling", and open the "Picto" view (you may need to search for it in the window options).
- To calculate the times for a model, open it and wait for the rendering to show in the Picto view (the progress animation in the bottom right indicates that the rendering is taking place).
- Once the view of the model is shown, the measurements are complete, and a new csv file would be generated besides the opened model (for instance, if the opened model is "models/genComps/gencomps-00.4K.model", a "models/genComps/gencomps-00.4K.model.profiling.csv" would be generated). Refresh the folder containing the model to see the new file.

## Plot the results

Once the standalone M2T transformation and all individual picto rendering measurements of a set of models have been taken, a plot containing a graph per model can be generated with the "plotscripts/process_and_plot.py" file. Usage instructions can be found inside the script.

To obtain plots of individual models, the "single_plot.py", "process_batch_results.py" and "process_picto_results.py" can be employed.
