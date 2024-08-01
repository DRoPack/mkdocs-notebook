# SPFx CSS

Microsoft uses CSS modules to ensure specificity of classes between `SPFx` solutions deployed on a SharePoint page by appending a # suffix to each class.  This ensures the classes are scoped to your webpart.

## CSS Override

To override the suffix being appended

```css Title="Global override"
: global {
    .welcome {
        text-align:  center;
    }
}
```
