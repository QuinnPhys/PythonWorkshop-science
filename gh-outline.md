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
- to verify “ls ~/.ssh” should see two files (private and public key)

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
