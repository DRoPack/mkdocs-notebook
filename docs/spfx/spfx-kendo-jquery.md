# SPFx with Kendo JQuery

Provide guidance on configuring an SPFx project to use Kendo UI JQuery.
This example shows using KendoGrid

```cmd title="Find Clink Directory"
C:\Users\blotter>clink info
```

## Config Folder

```json title="confg/config.json"
// Add the follwing to the externals attribute

"externals": {
    "jquery": {
    "path": "https://code.jquery.com/jquery-1.12.4.min.js",
    "globalName": "JQuery"
    },
    "kendo": {
    "path": "https://kendo.cdn.telerik.com/2024.4.1112/js/kendo.all.min.js",
    "globalName": "kendo",
    "globalDependencies": ["jquery"]
    }
}
```

## Package JSON

```json title="package.json"
// Example of the dependancies and devDependancies setup

"dependencies": {
    "@microsoft/sp-core-library": "~1.4.0",
    "@microsoft/sp-lodash-subset": "~1.4.0",
    "@microsoft/sp-office-ui-fabric-core": "~1.4.0",
    "@microsoft/sp-webpart-base": "~1.4.0",
    "@progress/kendo-ui": "^2024.4.1112",
    "@types/es6-promise": "0.0.33",
    "@types/webpack-env": "1.13.1",
    "jquery": "1.12.4"
},
"devDependencies": {
    "@microsoft/sp-build-web": "~1.4.1",
    "@microsoft/sp-module-interfaces": "~1.4.1",
    "@microsoft/sp-webpart-workbench": "~1.4.1",
    "@types/chai": "3.4.34",
    "@types/jquery": "^1.10.45",
    "@types/kendo-ui": "^2023.2.5",
    "@types/mocha": "2.2.38",
    "ajv": "~5.2.2",
    "gulp": "~3.9.1"
}
```

## TSConfig JSON

Configured for  ES2017

```json title="tsconfig.json"
{
  "compilerOptions": {
    "target": "es2017",  // Change from es5 to es2017
    "forceConsistentCasingInFileNames": true,
    "module": "commonjs",
    "moduleResolution": "node",
    "jsx": "react",
    "declaration": true,
    "sourceMap": true,
    "experimentalDecorators": true,
    "skipLibCheck": true,
    "typeRoots": ["./node_modules/@types", "./node_modules/@microsoft"],
    "types": ["es6-promise", "webpack-env"],
    "lib": ["es5", "dom", "es2017"]  // Ensure es2017 is included here
  }
}
```

## Web Part File

```ts title="src/webparts/PROJECTNAME/PROJECTNAMEWebPart.ts"
// Imports
import { SPComponentLoader } from "@microsoft/sp-loader";

// jQuery import
import * as $ from "jquery";

// Kendo-ui import
import "kendo";

//  Default class
export default class SpFxKendoJQueryDemoWebPart extends BaseClientSideWebPart<ISpFxKendoJQueryDemoWebPartProps> {
  public render(): void {
    SPComponentLoader.loadCss(
      "https://unpkg.com/@progress/kendo-theme-bootstrap@10.0.0/dist/bootstrap-main.css"
    );
 
    if(!this.renderedOnce){
    this.domElement.innerHTML = `
        <div id='ordersGrid'></div>
    `;
    }

    (<any>$("#ordersGrid")).kendoGrid({
      columns: [
        // The field matches the ID property in the data array.
        { field: "ProductID", title: "Product ID", width: "50px" },
        { field: "ProductName", title: "Product Name", width: "150px" },
        { field: "QuantityPerUnit", title: "Quanity", width: "200px" }
      ],
      dataSource: {
        data: Products,
        pageSize: 5
      },
      toolbar: ["search"],
      search: {
        fields: [
          { name: "ProductID", operator: "eq" },
          { name: "ProductName", operator: "contains" },
          { name: "QuantityPerUnit", operator: "contains" }
        ]
      },
      pageable: {
        pageSizes: [5, 10, 20, "all"]
        // alwaysVisible: true,
      }
    });
  }
```

!!! note
    Wrapping the `domElement` in `renderOnce` condition will ensure the div is not rendered multiple times.

    ```ts title="Rendered Once"
    public render(): void {
        if (!this.renderedOnce) {
            <div class="${ styles.container}">Blotter
            </div>
        }
    }
    ```
