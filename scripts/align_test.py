from Autodesk.Revit.UI import PostableCommand, RevitCommandId

uidoc = __revit__.ActiveUIDocument

align_comm = PostableCommand.Align
print(align_comm)

uidoc.Application.PostCommand(RevitCommandId.LookupPostableCommandId(PostableCommand.Align))