package org.chartapp;

import javafx.scene.paint.Color;
import javafx.scene.shape.Polygon;
import javafx.scene.text.Text;

public class FlowProcessor extends ChartObject{
    private Double width = 100.0;
    private Double height = 65.0;
    private Double offset = 20.0;
    private Polygon shape;
    private String label;
    private Color fillColor = Color.WHITESMOKE;
    private Color strokeColor = Color.BLACK;
    private Integer strokeWidth = 3;
    
    public FlowProcessor(String name) {
        super();
        label = name;
        genShape();
        Text text = new Text(label);
        getChildren().addAll(shape, text);
    }
    
    private void genShape() {
        Double w = (width-offset)/2;
        Double h = height/2;
        Double o = offset/2;
        shape = new Polygon(
            -w-o, -h,
            -w+o, h,
            w+o, h,
            w-o, -h
        );

        shape.setFill(fillColor);
        shape.setStroke(strokeColor);
        shape.setStrokeWidth(strokeWidth);
    }
}
