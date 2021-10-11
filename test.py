from cqmore import Workplane

polyline = (Workplane()
               .polylineJoin(
                   [(0, 0, 0), (10, 0, 0), (10, 0, 10), (10, 10, 10)], 
                   Workplane().box(1, 1, 1)
                )
           )