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

[NVM](docs\node\nvm.md)

## Check global packages installed

```cmd
    npm list -g --depth=0
```

[SharePoint 2019 Instructions](#sharepoint-2019-setup)

## Install Yeoman

[Yeoman Website](https://yeoman.io/)

Yeoman is a generic scaffolding system allowing the creation of any kind of app. It allows for rapidly getting started on new projects and streamlines the maintenance of existing projects.

Yeoman is language agnostic. It can generate projects in any language (Web, Java, Python, C#, etc.)

!!! warn
    The installed generator `Yeoman` does not need to match the installed version of the SharePoint Framework `SPFx`. <br>
    But wait, it does!!  For SharePoint 2019 on-premise the installed version of `Yeoman` needs to be yo@3.1.1

``` cmd
    npm install yo --global
```

## SharePoint 2019 Setup

[Andrew Connel Recommendation] (<https://www.voitanos.io/blog/definitive-guide-sharepoint-framework-sharepoint-server-2019/>)

 Development environment sweet spot for creating SPFx 1.4.1 projects for SharePoint Server 2019:

[x] Node.js LTS v8 (specifically, Node.js v8.17.0)
[x] Gulp-CLI v2.3.0
[x] Yeoman generator for the SharePoint Framework v1.10.0
[x] Yeoman v3.1.1

```cmd
    npm install gulp-cli@2.3.0 yo@3.1.1 @microsoft/generator-sharepoint@1.10.0 --global
``
