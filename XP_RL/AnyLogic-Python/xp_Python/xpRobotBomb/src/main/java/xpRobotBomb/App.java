package xpRobotBomb;

import robotbomb.*;
import java.util.*;
import java.util.regex.*;

public class App {

    static HashMap<String, Double> construct_q(String q_str) {
        // define q to be an empty Hash map
        HashMap<String, Double> q = new HashMap<String, Double>();
        // define temperary attylists
        ArrayList<String> keys = new ArrayList<String>();
        ArrayList<Double> values = new ArrayList<Double>();
        // get all state-action pairs as keys
        Pattern p = Pattern.compile("\\d-\\d-\\d-\\d-\\w");
        Matcher m = p.matcher(q_str);
        while (m.find()) {
            keys.add(m.group());
        }
        p = Pattern.compile("Delta-\\w");
        m = p.matcher(q_str);
        while (m.find()) {
            keys.add(m.group());
        }
        // get all q values
        p = Pattern.compile(":\\s([-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?),\\s"); //
        m = p.matcher(q_str);
        while (m.find()) {
            values.add(Double.parseDouble(m.group(1)));
        }
        // the last one
        p = Pattern.compile(":\\s([-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?)}");
        m = p.matcher(q_str);
        while (m.find()) {
            values.add(Double.parseDouble(m.group(1)));
        }
        // make Hash map
        for (int i = 0; i < keys.size(); i++) {
            q.put(keys.get(i), values.get(i));
        }
        return q;
    }

    public static void main(String[] args) {
        // system (Python) input
        Scanner scan = new Scanner(System.in);
        String q_str = scan.nextLine();
        q_str = q_str.toString();
        scan.close();
        // System.out.println(q_str);
        HashMap<String, Double> qValue = new HashMap<String, Double>();
        qValue = construct_q(q_str);
        // construct AnyLogic Experiment
        qUpdate ex = new qUpdate(null); /// note that qUpdate is the name of the simulation in AnyLogic
        ex.qValue = qValue;
        // run experiment
        ex.run();
        // get results
        System.out.println(ex.visitedStates);
        System.out.println(ex.takenActions);
        System.out.println(ex.returns);
    }
}
