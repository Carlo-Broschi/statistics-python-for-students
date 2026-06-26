from solid2 import polygon, rotate_extrude
profile_points = [
    (0, 0), (45, 0), (45, 6), (52, 68), (60, 70),
    (54, 70), (47, 66), (39, 8), (0, 8), (0, 0),
]
bowl = rotate_extrude(angle=360, _fn=120)(polygon(points=profile_points))
import inspect
print("save_as_scad" , hasattr(bowl, "save_as_scad"))
try:
    from solid2 import scad_render_to_file
    print("scad_render_to_file import OK")
except Exception as e:
    print("no scad_render_to_file:", e)
bowl.save_as_scad("test_chawan.scad")
print(open("test_chawan.scad").read()[:200])
