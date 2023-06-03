package org.chartapp;

import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;
import javafx.scene.text.Text;

public class FlowTerminator extends ChartObject{
    private Double width = 80.0;
    private Double height = 35.0;
    private Shape shape;
    private Color fillColor = Color.WHITESMOKE;
    private Color strokeColor = Color.BLACK;
    private Integer strokeWidth = 3;
    private Integer arcRadius = (int)(height/1);
    private String label;

    public FlowTerminator (String name) {
        super();
        label = name;
        genShape();
        Text text = new Text(label);
        getChildren().addAll(shape, text);
    }

    private void genShape() {
        Rectangle rect = new Rectangle(width, height);
        rect.setArcWidth(arcRadius);
        rect.setArcHeight(arcRadius);
        shape = rect;
        shape.setFill(fillColor);
        shape.setStroke(strokeColor);
        shape.setStrokeWidth(strokeWidth);
    }
}
