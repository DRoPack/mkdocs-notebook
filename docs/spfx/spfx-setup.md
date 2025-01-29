# Developer Environment Setup

## Compatibility Table

| SPFx   | Node.js (LTS) | TypeScript     | React  |
|--------|---------------|----------------|--------|
| 1.19.0 | v18           | v4.5, v4.7     | v17.0.1|
| 1.18.2 | v16, v18      | v4.5, v4.7     | v17.0.1|
| 1.18.1 | v16, v18      | v4.5, v4.7     | v17.0.1|
| ------ | ------        | ------         | ------ |
| 1.4.1  | v6, v8        | v2.4           | v15    | **SharePoint 2019

## NVM Setup and Commands

[NVM](../../node/nvm.md)

## Check global packages installed

Check which npm packages are installed on the current version of `Node` by running the following command.

```cmd title="List all npm packages"
npm list -g --depth=0
```

```cmd title="Check outdated npm packages"
npm outdated -g
```

``` cmd title="Get details of npm package"
npm info @microsoft/generator-sharepoint
```

## Install Node.Js

!!! note
    See above for `NVM` for installing Node.  The preference is to use `NVM` so multiple versions of `Node.js` can be installed on your development computer.

[SharePoint 2019 Setup](#sharepoint-2019-setup)

## Install Yeoman

[Yeoman Website](https://yeoman.io/)

Yeoman is a generic scaffolding system allowing the creation of any kind of app. It allows for rapidly getting started on new projects and streamlines the maintenance of existing projects.

Yeoman is language agnostic. It can generate projects in any language (Web, Java, Python, C#, etc.)

!!! warning
    The installed generator `Yeoman` does not need to match the installed version of the SharePoint Framework `SPFx`. <br>
    But wait, it does!!  For SharePoint 2019 on-premise the installed version of `Yeoman` needs to be yo@3.1.1

``` cmd
npm install yo --global
```

## Install TypeScript

TypeScript is installed by the generator locally to the project when `npm` install is run.

## Gulp

[Gulp Website](https://gulpjs.com/)

```cmd
npm install -g gulp-cli
```

!!! info
    All previous versions of `SPFx` starting with v1.12.1 are only supported with `Gulp v3`. Starting with `Node v12` and higher `Gulp v4` is only supported.

## SharePoint 2019 Setup

[Andrew Connel Recommendation](https://www.voitanos.io/blog/definitive-guide-sharepoint-framework-sharepoint-server-2019/)

Development environment sweet spot for creating SPFx 1.4.1 projects for SharePoint Server 2019:

- [x] Node.js LTS v8 (specifically, Node.js v8.17.0)
- [x] Gulp-CLI v2.3.0
- [x] Yeoman generator for the SharePoint Framework v1.10.0
- [x] Yeoman v3.1.1

```cmd
npm install gulp-cli@2.3.0 yo@3.1.1 @microsoft/generator-sharepoint@1.10.0 --global
```
