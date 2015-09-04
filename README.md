Houdini to Urho3d
-------
Currently this is a very bare bones exporter. Infact, at the moment i only have an example triangle working, until i spend a little more time one it.

This will export static meshes only!

Make a shelf tool, with some simple script

```
import urho
reload(urho)

urho.write_mdl()
```
select nodes that you want to export as mdl, and push the shelf tool.

To do:

everything.
Need to choose folder to write mdls into.
Mdls will be names based on the node selected.