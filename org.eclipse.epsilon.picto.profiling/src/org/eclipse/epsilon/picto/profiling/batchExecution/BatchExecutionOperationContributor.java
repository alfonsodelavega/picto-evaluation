package org.eclipse.epsilon.picto.profiling.batchExecution;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

import org.eclipse.epsilon.egl.IEgxModule;
import org.eclipse.epsilon.eol.execute.operations.contributors.OperationContributor;
import org.eclipse.epsilon.eol.types.EolNoType;
import org.eclipse.epsilon.picto.XmlHelper;

public class BatchExecutionOperationContributor extends OperationContributor {

	protected IEgxModule module;

	public BatchExecutionOperationContributor(IEgxModule module) {
		this.module = module;
	}

	@Override
	public boolean contributesTo(Object target) {
		return target == EolNoType.NoInstance;
	}

	public void dot2html(String dotFile) throws IOException, InterruptedException {

		ProcessBuilder pb = new ProcessBuilder(
				new String[] { "dot", "-T" + "svg", dotFile, "-o", dotFile + ".svg" });
		//		pb.inheritIO();
		Process p = pb.start();
		p.waitFor();

		String svgContents = new String(Files.readAllBytes(new File(dotFile + ".svg").toPath()));
		String htmlContents = "<html><body>" + removeXmlDeclaration(svgContents) + "</body></html>";

		Files.write(new File(dotFile + ".svg.html").toPath(), htmlContents.getBytes());
	}

	public void parallelDot2html(List<String> dotFiles) {
		dotFiles.parallelStream().forEach((dotFile) -> {
			try {
				dot2html(dotFile);
			}
			catch (IOException e) {
				e.printStackTrace();
			}
			catch (InterruptedException e) {
				e.printStackTrace();
			}
		});
	}

	public String getImage(String path) {
		return new File(module.getFile().getParent(), path).getAbsolutePath();
	}

	private String removeXmlDeclaration(String xml) {
		try {
			XmlHelper xmlHelper = new XmlHelper();
			return xmlHelper.getXml(xmlHelper.parse(xml));
		}
		catch (Exception ex) {
			return xml;
		}
	}
}
