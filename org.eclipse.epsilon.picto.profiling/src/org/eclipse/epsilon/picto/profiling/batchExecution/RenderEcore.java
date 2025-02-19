package org.eclipse.epsilon.picto.profiling.batchExecution;

import java.io.File;
import java.io.PrintStream;

import org.apache.commons.io.FileUtils;
import org.eclipse.epsilon.profiling.Stopwatch;

public class RenderEcore {

	public static void main(String[] args) throws Exception {

		// single-core run
		runTransformation(false);

		// parallel run
		runTransformation(true);

		System.out.println("Done");
	}

	public static void runTransformation(boolean parallelExecution) throws Exception {
		String modelsLocation = "models/ecore/%s";
		String[] models = { 
				"UML.ecore",
				"CIM15.ecore",
				"GluemodelEmoflonTTC2017.ecore",
				"RevEngSirius.ecore"
		};
		String metamodel = "models/ecore/Ecore.ecore";
		String transformationFile = "ecore2vis-standalone/ecore.egx";

		String outputFile = "batchRenderEcore.csv";
		if (parallelExecution) {
			outputFile = "batchRenderEcoreParallel.csv";
		}

		PrintStream profilingStream = new PrintStream(new File(outputFile));
		profilingStream.println("Model,BatchTimeMillis");

		int numReps = 10;
		// add some initial executions that won't be measured
		// avoids higher initial times due to low states of the cpu
		int notMeasuredExecutions = 3;
		numReps += notMeasuredExecutions;
		for (int rep = 0; rep < numReps; rep++) {
			// render every model in the list
			for (String modelName : models) {
				Stopwatch sw = new Stopwatch();
				sw.resume();
				ModelRenderer.render(modelsLocation, transformationFile, modelName, metamodel, parallelExecution);
				sw.pause();
				if (rep >= notMeasuredExecutions) {
					System.out.println(
							String.format("Rep %d: %s, parallel: %b, time: %d ms",
									rep - notMeasuredExecutions + 1,
									modelName,
									parallelExecution,
									sw.getElapsed()));
					profilingStream.println(String.format("%s,%d", modelName, sw.getElapsed()));
				}
			}
			// then, delete the output directory for a fresh next generation
			FileUtils.deleteDirectory(new File("gen"));
		}
		profilingStream.close();
	}
}
