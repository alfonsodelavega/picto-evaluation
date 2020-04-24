package org.eclipse.epsilon.picto.profiling.batchExecution;

import java.io.File;
import java.io.PrintStream;

import org.apache.commons.io.FileUtils;

public class RenderGenComps {

	public static void main(String[] args) throws Exception {
		String modelsLocation = "models/gencomps/%s";
		String[] models = {"gencomps-00.4K.model",
				"gencomps-01.5K.model", "gencomps-03.9K.model",
				"gencomps-05.8K.model", "gencomps-12.9K.model" };
		String metamodel = "models/ecore/comps.ecore";
		String transformationFile = "comps2vis-standalone/comps.egx";

		PrintStream profilingStream = new PrintStream(new File("batchRenderGenComps.csv"));
		profilingStream.println("Model,BatchTimeMillis");

		int numReps = 15;
		for (int i = 0; i < numReps; i++) {
			// render every model in the list
			for (String modelName : models) {
				System.out.println(String.format("Rep %d: %s", i + 1, modelName));
				long start = System.currentTimeMillis();
				ModelRenderer.render(modelsLocation, transformationFile, modelName, metamodel);
				long end = System.currentTimeMillis();
				profilingStream.println(String.format("%s,%d", modelName, end - start));
			}
			// then, delete the output directory for a fresh next generation
			FileUtils.deleteDirectory(new File("gen"));
		}
		profilingStream.close();
		System.out.println("Done");
	}
}
