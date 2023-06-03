package org.chartapp;
import javafx.scene.layout.GridPane;

public class Chart extends GridPane {
    public Chart() {
        super();
        setHgap(10);
        setVgap(10);
        

    }
    public void make_shape(String type, String label, int col, int row) {
        if (type == "output") {
            FlowOutput output = new FlowOutput(label);
            add(output, row, col);
        }
        if (type == "processor") {
            FlowProcessor processor = new FlowProcessor(label);
            add(processor, row, col);
        }
        if (type == "terminator") {
            FlowTerminator terminator = new FlowTerminator(label);
            add(terminator, row, col);
        }
        if (type == "decision") {
            FlowDecision decision = new FlowDecision(label);
            add(decision, row, col);
        }
    }
}
