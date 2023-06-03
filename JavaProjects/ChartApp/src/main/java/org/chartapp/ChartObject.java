package org.chartapp;

import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
// import javafx.scene.shape.Polygon;
import javafx.scene.shape.Shape;
import javafx.scene.text.Text;



public class ChartObject extends StackPane {
    private String label;
    private Double x;
    private Double y;
    private Shape shape;
    private Color fillColor = Color.WHITESMOKE;
    private Color strokeColor = Color.BLACK;

    public ChartObject(String name, Shape objectShape) {
        super();
        label = name;
        shape = objectShape;
        Text text = new Text(label);
        getChildren().addAll(shape, text);
        setShapeSettings();
    }
    
    public ChartObject() {
    }

    public void setObjectShape(Shape newShape) {
        shape = newShape;
    }

    public void setLabel(String newLabel) {
        label = newLabel;
    }

    public String getName() {
        return label;
    }

    public Double getX() {
        return x;
    }
    public Double getY() {
        return y;
    }

    public void setShapeSettings() {
        shape.setFill(fillColor);
        shape.setStroke(strokeColor);
        shape.setStrokeWidth(3);
    }
}




