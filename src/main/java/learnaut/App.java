package learnaut;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import de.learnlib.algorithm.PassiveLearningAlgorithm.PassiveDFALearner;
import de.learnlib.algorithm.rpni.BlueFringeRPNIDFA;
import net.automatalib.alphabet.*;
import net.automatalib.automaton.fsa.DFA;
import net.automatalib.visualization.Visualization;
import net.automatalib.word.Word;


public class App 
{
    private App() {
        // prevent instantiation
    }
    public static void main(String[] args) throws IOException {

        // define the alphabet
        final Alphabet<Character> alphabet = Alphabets.characters('a', 'b');

        final DFA<?, Character> model =
                computeModel(alphabet, getData().get(0), getData().get(1));
        Visualization.visualize(model, alphabet);
    }

    /**
     * Creates the learner instance, computes and return the inferred model.
     *
     * @param alphabet
     *         domain from which the learning data are sampled
     * @param positiveSamples
     *         positive samples
     * @param negativeSamples
     *         negative samples
     * @param <I>
     *         input symbol type
     *
     * @return the learned model
     */
    private static <I> DFA<?, I> computeModel(Alphabet<I> alphabet,
                                              Collection<Word<I>> positiveSamples,
                                              Collection<Word<I>> negativeSamples) {

        // instantiate learner
        // alternatively one can also use the EDSM variant (BlueFringeEDSMDFA from the learnlib-rpni-edsm artifact)
        // or the MDL variant (BlueFringeMDLDFA from the learnlib-rpni-mdl artifact)
        final PassiveDFALearner<I> learner = new BlueFringeRPNIDFA<>(alphabet);

        learner.addPositiveSamples(positiveSamples);
        learner.addNegativeSamples(negativeSamples);

        return learner.computeModel();
    }

    public static ArrayList<ArrayList<Word<Character>>> getData() throws IOException{
       BufferedReader br = new BufferedReader(new FileReader("/home/amadou/Desktop/learnAut/data.txt"));
       
       ArrayList<Word<Character>> listPlus = new ArrayList<Word<Character>>();
       ArrayList<Word<Character>> listMinus = new ArrayList<Word<Character>>();

       ArrayList<ArrayList<Word<Character>>> data = new ArrayList<ArrayList<Word<Character>>>();

       try {
            String line;
            boolean flag = true;
        
            while ((line = br.readLine()) != null) {
                if(line.equals("-")){
                    flag = false;
                }
                else{
                    if (flag){
                        listPlus.add(Word.fromString(line));
                    }
                    if (!flag){
                        listMinus.add(Word.fromString(line));
                    }
                }
            }
        } finally {
            br.close();
        }
        data.add(listPlus);
        data.add(listMinus);
        return data;
    }
}
