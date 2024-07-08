# NVM for Windows (Node Version Manager)

[GitHub - NVM](https://github.com/coreybutler/nvm-windows#readme)

## What is NVM?

NVM allows you to install different versions of Node, and switch between these versions depending on the project that you're working on via the command line.
In the next sections, I'll show you how to install NVM on your Windows, Linux, or Mac device.
Before proceeding, I also recommend that you uninstall Node.js if you have it installed already so that you do not have any conflicts with Node.js and nvm.

## NVM Commands

- nvm -v - Get Version
- nvm list - List all versions of Node installed
- nvm install latest - install the latest
- nvm install lts - install long term supported version
- nvm install X.Y.Z - install a specific version
- nvm use X.Y.Z - switch to a specific version
- nvm alias default X.Y.Z - make default node version

- nvm on/off - turns nvm on or off
- nvm uninstall X.Y.Z

## Install Dependencies

- After install of Node, switch to that Node version (nvm use X.Y.Z), then proceed to install dependencies on each version of Node.
  - **NPM**: `npm install -g` or `npm install -g npm@4.6.1`
  - [NPM Versions](https://www.npmjs.com/package/npm?activeTab=versions)
