package org.chartapp;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;




public class ChartApp extends Application {

    @Override
    public void start(Stage stage) throws Exception {
        Chart flowChart = new Chart();
        flowChart.setPrefSize(500, 500);
        Scene chartView = new Scene(flowChart);
        stage.setTitle("Chart Editor");
        stage.setScene(chartView);
        flowChart.make_shape("processor", "Process", 1, 1);
        flowChart.make_shape("output", "Display", 2, 1);
        flowChart.make_shape("decision", "Decide", 1, 2);
        flowChart.make_shape("terminator", "End", 2, 2);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }

}
