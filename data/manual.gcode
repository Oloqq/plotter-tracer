M140 S0 ; Bed temperature
M104 S0 ; Hotend temperature
M105 ; Report temperatures
M107 ; No fan
G92 E0 ; Reset Extruder
G1 F2700 E-5 ; Retract filament
G28 ; Home all axes
G0 F100 ; Set movement speed

G1 X100 Y100
G1 X120 Y100
G1 X120 Y120
G1 X100 Y120
G1 X100 Y100

M84 ; Disable all steppers

