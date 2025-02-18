# NVM for Windows (Node Version Manager)

[GitHub - NVM](https://github.com/coreybutler/nvm-windows#readme)

## What is NVM?

NVM allows you to install different versions of Node, and switch between these versions depending on the project that you're working on via the command line.

!!! warn "Previous Node Install"
  
    Before proceeding, It is recommend that you uninstall Node.js if you have it installed already. This will prevent any conflicts with Node.js and nvm.

## NVM Commands

| Command   | Description |
| --- | --- |
| :octicons-check-circle-fill-12:{ .greenCheck }  nvm -v | get Version |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm list | list all versions of Node installed |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm install latest | install the latest |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm install lts | install long term supported version |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm install X.Y.Z | install a specific version |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm use X.Y.Z | switch to a specific version |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm alias default X.Y.Z | make default node version |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm on/off | turns nvm on or off |
| :octicons-check-circle-fill-12:{ .greenCheck } nvm uninstall X.Y.Z |

## Install Dependencies

- After install of Node, switch to that Node version (nvm use X.Y.Z), then proceed to install dependencies on each version of Node.
  - **NPM**: `npm install -g` or `npm install -g npm@4.6.1`
  - [NPM Versions](https://www.npmjs.com/package/npm?activeTab=versions)
