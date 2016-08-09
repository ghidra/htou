make_alias(){
  #$1 FOLDER $2 LINKEDFOLDER $3 NEWFOLDER $4 OVERWRITE
  if [ ! -e $3 ];then
    #link does not exist, we can make it
    ln -s $2 $3
    echo "          -"$1" LINKED"
  else
    echo "          -"$1" link ALREADY EXISTS"
    if [ ! -z $4 ];then
     rm -f $3
     ln -s $2 $3
     echo "               -we replaced it anyway"
    fi
  fi
}

LINKPATH=`cd "$1"; pwd`
OVERWRITE=$2
DRYRUN=$3

if [ $# -eq 0 ];then
  echo "***********************************"
  echo "please provide path to houdini folder"
  echo "***********************************"
else
  if [ -d $LINKPATH ];then
    
    SCRIPT=$(readlink -f "$0")
    SCRIPTPATH=$(dirname "$SCRIPT")

    if [ ! -z "$DRYRUN" ];then
      echo "***********************************"
      echo "we are dryrunning it"
      echo "      LINKING"
      echo "      "$LINKPATH"/*.py"
      echo "      "$SCRIPTPATH"/*.py"
      echo "***********************************"
    else
      make_alias "export_urho" $SCRIPTPATH"/export_urho.py" $LINKPATH"/scripts/python/export_urho.py" $OVERWRITE
      make_alias "urho" $SCRIPTPATH"/urho.py" $LINKPATH"/scripts/python/urho.py" $OVERWRITE
      make_alias "urho_component" $SCRIPTPATH"/urho_component.py" $LINKPATH"/scripts/python/urho_component.py" $OVERWRITE
      make_alias "urho_utils" $SCRIPTPATH"/urho_utils.py" $LINKPATH"/scripts/python/urho_utils.py" $OVERWRITE
      make_alias "urho_xml" $SCRIPTPATH"/urho_xml.py" $LINKPATH"/scripts/python/urho_xml.py" $OVERWRITE
      make_alias "urho_shelf" $SCRIPTPATH"/urho3d.shelf" $LINKPATH"/toolbar/urho3d.shelf" $OVERWRITE
    fi
  fi

fi