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

        //define the alphabet

        ArrayList<Word<Character>> listPlus = getData().get(0);
        ArrayList<Word<Character>> listMinus = getData().get(1);

        ArrayList<Character> alphabet = new ArrayList<Character>();

        for (int i = 0; i < listPlus.size(); i++){
            for(int j = 0; j < listPlus.get(i).size(); j++){
                if (!alphabet.contains(listPlus.get(i).asList().get(j))){
                    alphabet.add(listPlus.get(i).asList().get(j));
                }
            }
        }

        for (int i = 0; i < listMinus.size(); i++){
            for(int j = 0; j < listMinus.get(i).size(); j++){
                if (!alphabet.contains(listMinus.get(i).asList().get(j))){
                    alphabet.add(listMinus.get(i).asList().get(j));
                }
            }
        }

        final Alphabet<Character> alph = Alphabets.fromList(alphabet);

        final DFA<?, Character> model = computeModel(alph, listPlus, listMinus);
            

        Visualization.visualize(model, alph);
    }


    // private static <I> DFA<?, I> computeModel(Alphabet<I> alphabet,
    //         Collection<Word<I>> positiveSamples,
    //         Collection<Word<I>> negativeSamples) {

    //     // instantiate learner
    //     // alternatively one can also use the EDSM variant (BlueFringeEDSMDFA from the learnlib-rpni-edsm artifact)
    //     // or the MDL variant (BlueFringeMDLDFA from the learnlib-rpni-mdl artifact)
    //     final PassiveDFALearner<I> learner = new BlueFringeRPNIDFA<>(alphabet);                      

    //     learner.addPositiveSamples(positiveSamples);
    //     learner.addNegativeSamples(negativeSamples);

    //     return learner.computeModel();
    // }

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
        long startTimePTA = System.nanoTime();
        final PassiveDFALearner<I> learner = new BlueFringeRPNIDFA<>(alphabet);
        long endTimePTA = System.nanoTime();                      

        double timePTA = (endTimePTA - startTimePTA) / 1000000000.;
        System.out.println("Time PTA : " + timePTA);

        learner.addPositiveSamples(positiveSamples);
        learner.addNegativeSamples(negativeSamples);


        long startTimeModel = System.nanoTime();
        DFA<?, I> model = learner.computeModel();
        long endTimeModel = System.nanoTime();

        double timeModel = (endTimeModel - startTimeModel) / 1000000000.;

        System.out.println("Time Model : " + timeModel);
        System.out.println("Nb states : "+ model.size());
        return model;
    }
    

    public static ArrayList<ArrayList<Word<Character>>> getData() throws IOException{
       BufferedReader br = new BufferedReader(new FileReader("data.txt"));
       
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
