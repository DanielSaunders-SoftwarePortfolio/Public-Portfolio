module ChartApp {
    requires javafx.controls;
    requires javafx.fxml;
    requires transitive javafx.graphics;
    opens org.chartapp to javafx.fxml;
    exports org.chartapp;
}
