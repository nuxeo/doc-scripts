This compiles the Javadoc documentation, and pushes it to a remote server.

Usage: ./update-javadoc

To force hg update to use -C, define environment variable FORCE_CLEAN_UPDATE=y
To force a full rebuild (takes a long time), define environment variable FORCE_BUILD=y 
To only do the rsync, define environment variable SYNC_ONLY=y
To not do the rsync, define environment variable NO_SYNC=y
