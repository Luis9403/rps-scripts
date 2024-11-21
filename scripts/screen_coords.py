uiapp = __revit__

vr = uiapp.DrawingAreaExtents
# Bottom right
x_br = vr.Right
y_br = vr.Bottom

print(x_br, y_br)

# Top left
x_tl = vr.Left
y_tl = vr.Top

print(x_tl, y_tl)

# Bottom left
x_bl = vr.Left
y_bl = vr.Bottom

print(x_bl, y_bl)