package exp01;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.*;

public final class Result {

    // The 3 candidate sorting algorithms
    static final String[] ALGOS = {"UntilNoChange", "WhileNeeded", "PassPerItem"};
    static final String[] ORDERINGS = {"random", "sorted", "reverse"};
    static final int[] SIZES = {1000, 5000}; // Array sizes
    static final int REPETITIONS = 10;       // Repetitions per condition

    public static void main(String[] args) throws Exception {
        System.out.println("====================================================");
        System.out.println(" BUBBLE SORT BENCHMARK ");
        System.out.println("====================================================");

        // 1. WARM-UP (Stabilizes the JIT compiler before measuring)
        System.out.print("Warming up JVM...");
        Random warmRnd = new Random(123);
        for (String algo : ALGOS) {
            for (int i = 0; i < 15; i++) {
                Integer[] a = createArray("random", 1000, warmRnd);
                getSorter(algo).sort(a);
            }
        }
        System.out.println(" Done!\n");

        // 2. RUN EXPERIMENT AND SAVE TO CSV
        PrintWriter csv = new PrintWriter(new FileWriter("results.csv"));
        csv.println("Trial,Algorithm,ArraySize,InputOrdering,ExecutionTimeMs");

        System.out.printf("%-15s | %-8s | %-6s | %-12s%n", "Algorithm", "Order", "Size", "Time (ms)");
        System.out.println("----------------------------------------------------");

        for (int rep = 1; rep <= REPETITIONS; rep++) {
            for (String ord : ORDERINGS) {
                for (int size : SIZES) {
                    // Generate master test array
                    Random rnd = new Random(rep * 1000L + size);
                    Integer[] master = createArray(ord, size, rnd);

                    // Test all 3 algorithms on the EXACT same array
                    for (String algoName : ALGOS) {
                        Integer[] copy = master.clone();
                        Sorter<Integer> sorter = getSorter(algoName);

                        long start = System.nanoTime();
                        sorter.sort(copy);
                        long end = System.nanoTime();

                        double timeMs = (end - start) / 1_000_000.0;

                        // Save row to CSV
                        csv.printf(Locale.ROOT, "%d,%s,%d,%s,%.4f%n", rep, algoName, size, ord, timeMs);

                        // Print to terminal
                        System.out.printf("%-15s | %-8s | %-6d | %10.4f ms%n", algoName, ord, size, timeMs);
                    }
                }
            }
            System.out.println("--> Replicate " + rep + " of " + REPETITIONS + " completed.");
        }

        csv.close();
        System.out.println("====================================================");
        System.out.println("FINISHED! Results saved to results.csv");
        System.out.println("====================================================");
    }

    // Factory method to instantiate candidate sorters
    static Sorter<Integer> getSorter(String name) {
        if (name.equals("UntilNoChange")) return new BubbleSortUntilNoChange<>();
        if (name.equals("WhileNeeded"))   return new BubbleSortWhileNeeded<>();
        return new BubbleSortPassPerItem<>();
    }

    // Generates input arrays with specific orderings
    static Integer[] createArray(String ordering, int n, Random rnd) {
        Integer[] arr = new Integer[n];
        for (int i = 0; i < n; i++) arr[i] = rnd.nextInt(100_000);

        if (ordering.equals("sorted")) {
            Arrays.sort(arr);
        } else if (ordering.equals("reverse")) {
            Arrays.sort(arr);
            Collections.reverse(Arrays.asList(arr));
        }
        return arr;
    }
}