package org.eclipse.epsilon.picto.profiling.batchExecution;

import java.io.File;
import java.net.URISyntaxException;

import org.eclipse.epsilon.common.parse.problem.ParseProblem;
import org.eclipse.epsilon.common.util.StringProperties;
import org.eclipse.epsilon.egl.EgxModule;
import org.eclipse.epsilon.emc.emf.EmfModel;
import org.eclipse.epsilon.eol.exceptions.models.EolModelLoadingException;
import org.eclipse.epsilon.eol.execute.context.Variable;
import org.eclipse.epsilon.eol.models.IRelativePathResolver;
import org.eclipse.epsilon.eol.types.EolPrimitiveType;

public class ModelRenderer {

	public static void render(String modelsLocation, String transformationFile,
			String modelName, String metamodel) throws Exception {

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
						metamodel,
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
		properties.put(EmfModel.PROPERTY_FILE_BASED_METAMODEL_URI,
				new File(metamodel).toURI().toString());
		properties.put(EmfModel.PROPERTY_MODEL_URI,
				new File(model).toURI().toString());
		properties.put(EmfModel.PROPERTY_READONLOAD, readOnLoad + "");
		properties.put(EmfModel.PROPERTY_STOREONDISPOSAL,
				storeOnDisposal + "");
		emfModel.load(properties, (IRelativePathResolver) null);
		return emfModel;
	}
}
