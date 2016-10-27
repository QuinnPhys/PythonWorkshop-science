LECTURE 0 notes:



# USING GITHUB #
- Sign up for github 
- Go to education.github.com to request free private repositories (requires email verification)
- create repository, initialize with README, add .gitignore for python
- to clone repository need SSH key —> 

## SSH KEY ##
- open Terminal
- “ssh-keygen”
- save in default key
- enter passphrase
NOW you have a SSH key
- to verify ``ls ~/.ssh`` should see two files (private and public key)

## RETURN TO GITUB ##
- settings
- add SSH key
- Title of specific machine to identify key
- copy entire public key (view in Terminal with command ``cat ~/.ssh/id_rsa.pub``)
(ENTIRE key including ssh-rsa and other wireless.edu junk)

## NOW TO CLONE REPOSITORY ##
- return to main github page
- copy the clone URL
- return to Terminal, choose location for clone (I put it on the desktop “cd Desktop”)
- clone with “git clone <paste URL>”
- May need to install some developer junk on OS X for git (redo previous step after)
- type “yes” if not worried about authenticity of host
- NOW REPO is cloned to local

## GIT COMMANDS ##
To be executed from the command line
- ``git status`` status of modified files within local repository
- ``git pull`` pulls remote commit (repository) to local
In order to push local commit (repository) to remote, one must first add modified files to the "staging area."
- ``git add <file>`` add file to staging area
- ``git commit -m "description_of_changes"`` to commit (update local repository)
- ``git push`` to push local commit (repository) to remote
- ``git push`` pushes local commit (repository) to remote