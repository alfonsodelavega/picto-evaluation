package org.eclipse.epsilon.picto.profiling.batchExecution;

import java.io.File;
import java.io.PrintStream;
import java.net.URISyntaxException;

import org.apache.commons.io.FileUtils;
import org.eclipse.epsilon.common.parse.problem.ParseProblem;
import org.eclipse.epsilon.common.util.StringProperties;
import org.eclipse.epsilon.egl.EgxModule;
import org.eclipse.epsilon.emc.emf.EmfModel;
import org.eclipse.epsilon.eol.exceptions.models.EolModelLoadingException;
import org.eclipse.epsilon.eol.execute.context.Variable;
import org.eclipse.epsilon.eol.models.IRelativePathResolver;
import org.eclipse.epsilon.eol.types.EolPrimitiveType;

public class RenderModels {

	public static void main(String[] args) throws Exception {
		String modelsLocation = "models/%s";
		String[] models = { "comps.ecore", "Ecore.ecore" };
		String transformationFile = "ecore2vis-standalone/ecore.egx";

		PrintStream profilingStream = new PrintStream(new File("batchResults.csv"));
		profilingStream.println("Model,BatchTimeMillis");

		int numReps = 20;
		for (int i = 0; i < numReps; i++) {
			// render every model in the list
			for (String modelName : models) {
				long start = System.currentTimeMillis();
				renderModel(modelsLocation, transformationFile, modelName);
				long end = System.currentTimeMillis();
				profilingStream.println(String.format("%s,%d", modelName, end - start));
			}
			// then, delete the output directory for a fresh next generation
			FileUtils.deleteDirectory(new File("gen"));
		}
		profilingStream.close();
		System.out.println("Done");
	}

	private static void renderModel(String modelsLocation, String transformationFile, String modelName)
			throws Exception {

		EgxModule module = new EgxModule("org.eclipse.epsilon.picto.profiling");
		module.parse(new File(transformationFile).getAbsoluteFile());
		if (!module.getParseProblems().isEmpty()) {
			System.err.println("The following errors were identified");
			for (ParseProblem parseProblem : module.getParseProblems()) {
				System.err.println("- " + parseProblem);
			}
			return;
		}

		module.getContext().getFrameStack().put(
				new Variable("modelName", modelName, EolPrimitiveType.String));
		module.getContext().getOperationContributorRegistry().add(
				new BatchExecutionOperationContributor(module));

		EmfModel emfModel =
				createEmfModel("M",
						String.format(modelsLocation, modelName),
						"http://www.eclipse.org/emf/2002/Ecore",
						true, false);
		module.getContext().getModelRepository().addModel(emfModel);

		module.execute();
	}

	protected static EmfModel createEmfModel(String name, String model,
			String metamodel, boolean readOnLoad, boolean storeOnDisposal)
			throws EolModelLoadingException, URISyntaxException {
		EmfModel emfModel = new EmfModel();
		StringProperties properties = new StringProperties();
		properties.put(EmfModel.PROPERTY_NAME, name);
		properties.put(EmfModel.PROPERTY_METAMODEL_URI, metamodel);
		properties.put(EmfModel.PROPERTY_MODEL_URI,
				new File(model).toURI());
		properties.put(EmfModel.PROPERTY_READONLOAD, readOnLoad + "");
		properties.put(EmfModel.PROPERTY_STOREONDISPOSAL,
				storeOnDisposal + "");
		emfModel.load(properties, (IRelativePathResolver) null);
		return emfModel;
	}
}
