/*
Classify text as bullying trace or not.

Input: each line from stdin is treated as a short document.  It is expected that the input
has been filtered by Enrichment.jar to remove lines without bullying keywords.  This program
will still work if no filtering has been done, but may produce warnings to stderr.

Output: The program runs SVM classification and outputs the margin of the input lines to stdout.
A positive margin means that the line is classified as a bullying trace.

Warnings: the program is intended to work on "enriched tweets."  It will try to detect whether an
input line is such a tweet.  If not, it produces a warning message for that line.  it will still 
attempt to classify the line.  However, the classification accuracy in the presence of a warning
can not be guaranteed.

To cite the code:

Learning from bullying traces in social media
Jun-Ming Xu, Kwang-Sung Jun, Xiaojin Zhu, and Amy Bellmore
In North American Chapter of the Association for Computational Linguistics - 
Human Language Technologies (NAACL HLT)
Montreal, Canada, 2012

Author: Jun-Ming Xu (xujm@cs.wisc.edu)

Contact: Jun-Ming Xu (xujm@cs.wisc.edu), Xiaojin Zhu (jerryzhu@cs.wisc.edu)
June 2012

*/

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class Classification {

	static String[] keywords = { "ignored", "pushed", "rumors", "locker",
			"spread", "shoved", "rumor", "teased", "kicked", "crying",
			"bullied", "bully", "bullyed", "bullying", "bullyer", "bulling" };

	double[] w;

	public static void main(String[] args) {
		String line = null;
		ArrayList<String> tokens = null;
		Tokenizer tokenizer = new Tokenizer();

		Tokens2FeatureVector t2v = new Tokens2FeatureVector();
		t2v.loadVocab("model/vocab");

		Classification classifier = new Classification();
		classifier.loadModel("model/model");

		try {
			BufferedReader br = new BufferedReader(new InputStreamReader(
					System.in));
			while ((line = br.readLine()) != null) {
				checkInput(line);
				tokens = tokenizer.tokenize(line);
				t2v.covertFeatureVector(tokens);
				System.out.println(classifier.classify(t2v.getIndexSet(), t2v
						.getValueSet()));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// Since the model is trained on the enriched data, the test data should be
	// also in the enriched data 'containing keywords'.
	// Otherwise, the performance is not guaranteed.
	public static boolean checkInput(String text) {
		if (text.length() > 150) {
			System.err.println("(Warning: line longer than 150 characters): " + text);
			return false;
		}
		String lowerCase = text.toLowerCase();
		boolean containKeyword = false;
		for (String k : keywords)
			if (lowerCase.contains(k)) {
				containKeyword = true;
				break;
			}
		if (containKeyword == false) {
			System.err.println("(Warning: line does not contain keywords): " + text);
			return false;
		}
		if (!lowerCase.contains("bull")) {
			System.err.println("(Warning: line does not contain string \"bull\"): " + text);
			return false;
		}
		if (text.contains("RT")) {
			System.err.println("(Warning: line contains \"RT\", retweet?): " + text);
			return false;
		}
		return true;
	}

	public void loadModel(String file) {
		try {
			BufferedReader br = new BufferedReader(new InputStreamReader(
					Classification.class.getResourceAsStream(file)));
			String line = null;
			boolean readingSV = false;
			while ((line = br.readLine()) != null) {
				String[] tokens = line.split("[ :]");
				if (readingSV) {
					double ay = Double.parseDouble(tokens[0]);
					for (int i = 1; i < tokens.length - 1; i += 2) {
						int index = Integer.parseInt(tokens[i]);
						double value = Double.parseDouble(tokens[i + 1]);
						w[index] += ay * value;
					}
					continue;
				}
				if (line.contains("# highest feature index "))
					w = new double[Integer.parseInt(tokens[0]) + 1];
				else if (line.contains("# threshold b")) {
					w[0] = -Double.parseDouble(tokens[0]);
					readingSV = true;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public double classify(Integer[] index, double[] value) {
		double margin = w[0];
		for (int i : index)
			margin += w[i] * value[i];
		return margin;
	}

}
