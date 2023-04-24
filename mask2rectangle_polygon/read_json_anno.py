"""
2020.09.18:alian
json_to_xml
"""
# -*- coding: utf-8 -*-
import numpy as np
import json


class ReadAnno:
    def __init__(self, json_path, process_mode="rectangle"):
        self.json_data = json.load(open(json_path))
        self.filename = self.json_data['imagePath']
        self.width = self.json_data['imageWidth']
        self.height = self.json_data['imageHeight']

        self.coordis = []
        assert process_mode in ["rectangle", "polygon"]
        if process_mode == "rectangle":
            self.process_polygon_shapes()
        elif process_mode == "polygon":
            self.process_polygon_shapes()

    def process_rectangle_shapes(self):
        for single_shape in self.json_data['shapes']:
            bbox_class = single_shape['label']
            xmin = single_shape['points'][0][0]
            ymin = single_shape['points'][0][1]
            xmax = single_shape['points'][1][0]
            ymax = single_shape['points'][1][1]
            self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])

    def process_polygon_shapes(self):
        for single_shape in self.json_data['shapes']:
            bbox_class = single_shape['label']
            temp_points = []
            for couple_point in single_shape['points']:
                x = float(couple_point[0])
                y = float(couple_point[1])
                temp_points.append([x, y])
            temp_points = np.array(temp_points)
            xmin, ymin = temp_points.min(axis=0)
            xmax, ymax = temp_points.max(axis=0)
            self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])

    def get_width_height(self):
        return self.width, self.height

    def get_filename(self):
        return self.filename

    def get_coordis(self):
        return self.coordis
